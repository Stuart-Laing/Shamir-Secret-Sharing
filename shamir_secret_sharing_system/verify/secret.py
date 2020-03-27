from ..constants import SECRET_STRING_MIN_LEN, SECRET_STRING_MAX_LEN
from ..errors import SecretStringLengthError, SecretStringEncodingError


__all__ = ["Secret"]


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
            raise SecretStringLengthError(
                f"secret_string cannot be shorter than {self.min_length} characters")
        elif len(self.secret_string) > self.max_length:
            raise SecretStringLengthError(
                f"secret_string cannot be longer than {self.max_length} characters")

    def check_chars(self):
        for character in self.secret_string:
            if ord(character) > 255:
                raise SecretStringEncodingError("All characters must be able to be represented by two hex digits")
