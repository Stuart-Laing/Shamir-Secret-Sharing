import re
import os
import shamir_secret_sharing_system


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
            raise shamir_secret_sharing_system.errors.PartsFileCountError(
                "Chosen file does not contain enough entries")

        if self.base == 2:
            allowed_chars = ("0", "1")

        elif self.base == 10:
            allowed_chars = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        elif self.base == 16:
            allowed_chars = ("A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f",
                             "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        elif self.base == 64:
            allowed_chars = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                             "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                             "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/")

        else:
            allowed_chars = "kill"

        valid_base = re.compile(r"^\d+\040[A-Za-z0-9+/]+$")

        for line_no, line in enumerate(lines):
            line_match_obj = valid_base.search(line)

            if line_match_obj is None:
                raise shamir_secret_sharing_system.errors.PartsFileFormatError(
                    "Parts File must be in the format '<PartNum> <PartValue>' 1 per line")

            for value_char in line_match_obj.group().split(" ")[1]:
                if value_char not in allowed_chars:
                    raise shamir_secret_sharing_system.errors.PartsFileBaseError(
                        f"Part value at line no {line_no + 1} is not of the expected base")


class Base:
    def __init__(self, base):
        pass


class Secret:
    def __init__(self, secret_string):
        pass


class NAndK:
    def __init__(self, total_parts, min_for_reconstruct):
        pass


class FieldLimit:
    def __init__(self, field_limit, base):
        pass