import shamir_secret_sharing_system


class Secret:
    def __init__(self, secret_string):

        # Things to check
        # secret is a string
        # Secret is not too short
        # Secret is not too long
        # Each character can be represented by two hex digits

        self.secret_string = secret_string
        self.min_length = shamir_secret_sharing_system.constants.SECRET_STRING_MIN_LEN
        self.max_length = shamir_secret_sharing_system.constants.SECRET_STRING_MAX_LEN

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
