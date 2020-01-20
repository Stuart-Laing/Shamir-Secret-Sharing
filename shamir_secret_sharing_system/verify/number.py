import shamir_secret_sharing_system


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
