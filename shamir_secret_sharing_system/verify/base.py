import shamir_secret_sharing_system


class Base:
    def __init__(self, base, command_line_arg=False):
        """
        Creates the object and calls each check function to verify it

        :param base: int, str The base that the user wishes to use
        :param command_line_arg: bool Specifies whether the base is being given directly from sys.args or from a function
        """

        # Things to check
        # The base is in the form of a number, even if its the string "16"
        # The base is one of the supported bases

        self.base = base
        self.allowed_bases = shamir_secret_sharing_system.constants.SUPPORTED_BASES

        self.check_is_num(command_line_arg)
        self.check_if_allowed()

    def check_is_num(self, num_is_string):
        if num_is_string:
            if not isinstance(self.base, str):
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
