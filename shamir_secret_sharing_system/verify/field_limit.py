from . import Number
from ..errors import ValueNotOfSpecifiedBaseError


__all__ = ["FieldLimit"]


class FieldLimit:
    def __init__(self, field_limit, base):
        # field_limit check will only be used in __main__.py
        # Therefore field_limit will always be a string

        # Things to check
        # The value if its in a different base is valid for the given base

        try:
            Number(field_limit, base)

        except ValueNotOfSpecifiedBaseError:
            raise ValueError("Field_limit cannot be converted from given base")
