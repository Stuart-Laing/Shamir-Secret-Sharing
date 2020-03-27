from ..errors import PartsFileCountError, PartsFileFormatError, PartsFileBaseError, ValueNotOfSpecifiedBaseError
from . import Number

import re
import os


__all__ = ["PartsFile"]


class PartsFile:
    def __init__(self, file_path, base):
        # Things to check
        # file path is actually a string
        # Permissions to read the file
        # File exists
        # File is in the correct format
        # File has at least 2 entries
        # File is actually a text file

        # base can be assumed to be correct at this stage

        self.file_path = file_path
        self.base = base

        self.check_file_path_type()
        self.check_exists()
        self.check_if_file()
        self.check_permissions()
        self.check_format()

    def check_file_path_type(self):
        if not isinstance(self.file_path, str):
            raise TypeError("file_path must be of type str")

    def check_exists(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError("Chosen File does not exist")

    def check_if_file(self):
        if not os.path.isfile(self.file_path):
            raise FileExistsError("Chosen File does not exist")

    def check_permissions(self):
        try:
            parts_file = open(self.file_path, "r")
        except PermissionError:
            raise PermissionError("Chosen file cannot be read from")

        parts_file.close()

    def check_format(self):
        with open(self.file_path, "r") as parts_file:
            lines = [line.strip() for line in parts_file.readlines()]

        if len(lines) < 2:
            raise PartsFileCountError(
                "Chosen file does not contain enough entries")

        valid_base = re.compile(r"^\d+\040[A-Za-z0-9+/]+$")

        for line_no, line in enumerate(lines):
            line_match_obj = valid_base.search(line)

            if line_match_obj is None:
                raise PartsFileFormatError(
                    "Parts File must be in the format '<PartNum> <PartValue>' 1 per line")

            try:
                Number(line_match_obj.group().split(" ")[1], self.base)
            except ValueNotOfSpecifiedBaseError:
                raise PartsFileBaseError(
                    f"Part value at line no {line_no + 1} is not of the expected base")
