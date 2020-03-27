from ..errors import UnrecoverableSecretError


__all__ = ["NAndK"]


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
            raise UnrecoverableSecretError(
                "Secret would be unrecoverable if less parts are created than needed to retrieve secret")

    def check_valid_polynomial(self):
        if self.min_for_reconstruct < 2:
            raise ValueError("Creating a part list of length one would just be the secret")
