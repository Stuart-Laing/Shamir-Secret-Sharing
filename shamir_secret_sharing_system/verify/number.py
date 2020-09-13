from ..errors import ValueNotOfSpecifiedBaseError


__all__ = ["Number"]


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

        else:
            # Should never happen as base is validated by this point
            self.allowed_chars = ()

        for digit in self.number:
            if digit not in self.allowed_chars:
                raise ValueNotOfSpecifiedBaseError("Given number cannot be converted to the given base")
