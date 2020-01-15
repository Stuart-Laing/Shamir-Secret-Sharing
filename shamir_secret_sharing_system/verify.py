import re
import os
import shamir_secret_sharing_system


SUPPORTED_BASES = (10, 16)
SECRET_STRING_MIN_LEN = 1
SECRET_STRING_MAX_LEN = 200


class Number:
    def __init__(self, number, base):

        self.number = number
        self.base = base

        # if self.base == 2:
        #     self.allowed_chars = ("0", "1")

        if self.base == 10:
            self.allowed_chars = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        elif self.base == 16:
            self.allowed_chars = ("A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f",
                                  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        # elif self.base == 64:
        #     self.allowed_chars = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        #                           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        #                           "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        #                           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        #                           "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/")
        else:
            # Should never happen as base is validated by this point
            self.allowed_chars = ()

        for digit in self.number:
            if digit not in self.allowed_chars:
                raise shamir_secret_sharing_system.errors.ValueNotOfSpecifiedBaseError(
                    "Given number cannot be converted to the given base")


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

        valid_base = re.compile(r"^\d+\040[A-Za-z0-9+/]+$")

        for line_no, line in enumerate(lines):
            line_match_obj = valid_base.search(line)

            if line_match_obj is None:
                raise shamir_secret_sharing_system.errors.PartsFileFormatError(
                    "Parts File must be in the format '<PartNum> <PartValue>' 1 per line")

            try:
                Number(line_match_obj.group().split(" ")[1], self.base)
            except ValueError:
                raise shamir_secret_sharing_system.errors.PartsFileBaseError(
                    f"Part value at line no {line_no + 1} is not of the expected base")


class Base:
    def __init__(self, base, command_line_arg=False):
        """
        Creates the object and calls each check function to verify it

        :param base: int, str The base that the user wishes to use
        :param command_line_arg: Specifies whether the base is being given directly from sys.args or from a function
        """

        # Things to check
        # The base is in the form of a number, even if its the string "16"
        # The base is one of the supported bases

        self.base = base
        self.allowed_bases = SUPPORTED_BASES

        self.check_is_num(command_line_arg)
        self.check_if_allowed()

    def check_is_num(self, allowed_to_be_string):
        if allowed_to_be_string:
            if not isinstance(self.base, (str, int)):
                raise TypeError("base must be of type int or convertible to one")
            try:
                self.base = int(self.base)
            except ValueError:
                raise TypeError("base must be of type int or convertible to one")

        else:
            if not isinstance(self.base, int):
                raise TypeError("base must be of type int")

    def check_if_allowed(self):
        if self.base not in self.allowed_bases:
            raise shamir_secret_sharing_system.errors.BaseNotSupportedError(
                f"Given base is not in the list of supported bases : {self.allowed_bases}")


class Secret:
    def __init__(self, secret_string):

        # Things to check
        # secret is a string
        # Secret is not too short
        # Secret is not too long
        # Each character can be represented by two hex digits

        self.secret_string = secret_string
        self.min_length = SECRET_STRING_MIN_LEN
        self.max_length = SECRET_STRING_MAX_LEN

        self.check_type()
        self.check_length()
        self.check_chars()

    def check_type(self):
        if not isinstance(self.secret_string, str):
            raise TypeError("secret_string must be of type str")

    def check_length(self):
        if len(self.secret_string) < self.min_length:
            raise shamir_secret_sharing_system.errors.SecretStringLengthError(
                f"secret_string cannot be shorter than {self.min_length} characters")
        elif len(self.secret_string) > self.max_length:
            raise shamir_secret_sharing_system.errors.SecretStringLengthError(
                f"secret_string cannot be longer than {self.max_length} characters")

    def check_chars(self):
        for character in self.secret_string:
            if ord(character) > 255:
                raise shamir_secret_sharing_system.errors.SecretStringEncodingError(
                    "All characters must be able to be represented by two hex digits")


class NAndK:
    def __init__(self, total_parts, min_for_reconstruct, command_line_arg=False):

        # Things to check
        # The values are in the form of a number, even if its the string "14"
        # N is larger or equal to K
        # K is not less than 2

        self.total_parts = total_parts
        self.min_for_reconstruct = min_for_reconstruct

        self.check_is_num(self.total_parts, command_line_arg)
        self.check_is_num(self.min_for_reconstruct, command_line_arg)

        self.total_parts = int(self.total_parts)
        self.min_for_reconstruct = int(self.min_for_reconstruct)

        self.check_n_relation_to_k()
        self.check_valid_polynomial()

    @staticmethod
    def check_is_num(number, allowed_to_be_string):
        if allowed_to_be_string:
            if not isinstance(number, (str, int)):
                raise TypeError("total_parts and min_for_reconstruct must be of type int or convertible to one")
            try:
                int(number)
            except ValueError:
                raise TypeError("total_parts and min_for_reconstruct must be of type int or convertible to one")

        else:
            if not isinstance(number, int):
                raise TypeError("total_parts and min_for_reconstruct must be of type int")

    def check_n_relation_to_k(self):
        if self.total_parts < self.min_for_reconstruct:
            raise shamir_secret_sharing_system.errors.UnrecoverableSecretError(
                "Secret would be unrecoverable if less parts are created than needed to retrieve secret")

    def check_valid_polynomial(self):
        if self.min_for_reconstruct < 2:
            raise ValueError("Creating a part list of length one would just be the secret")


class FieldLimit:
    def __init__(self, field_limit, base):
        # field_limit check will only be used in __main__.py
        # Therefore field_limit will always be a string

        # Things to check
        # The value if its in a different base is valid for the given base

        try:
            Number(field_limit, base)

        except ValueError:
            raise ValueError("Field_limit cannot be converted from given base")
