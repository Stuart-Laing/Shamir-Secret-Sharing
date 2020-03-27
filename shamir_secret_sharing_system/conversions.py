from .errors import BaseNotSupportedError, ValueNotOfSpecifiedBaseError
from .verify import Base, Number, Secret


from typing import Union


def base_converter(number: Union[str, int], current_base: int, target_base: int) -> Union[str, int]:
    """
    Converts the given number from its current base to the target base

    :param number: str, int The number to be converted
    :param current_base: int The current base the given number is in
    :param target_base: int The target base the number will be converted to
    :returns output_number: str The number after being converted
    """

    if not isinstance(number, (str, int)):
        raise TypeError("number must be of type str or int")
    if not isinstance(current_base, int):
        raise TypeError("current_base must be of type int")
    if not isinstance(target_base, int):
        raise TypeError("target_base must be of type int")

    try:
        Base(current_base)
    except BaseNotSupportedError:
        raise BaseNotSupportedError("Current base is not supported")

    try:
        Base(target_base)
    except BaseNotSupportedError:
        raise BaseNotSupportedError("Target base is not supported")

    try:
        Number(str(number), current_base)
    except ValueNotOfSpecifiedBaseError:
        raise ValueNotOfSpecifiedBaseError("Given number is not of the base specified")

    # Currently only supporting converting number to hex
    number = str(number).lower()
    number_base10 = int(number, current_base)

    if target_base == 10:
        return number_base10
    elif target_base == 16:
        return hex(number_base10)[2:]


def string_to_integer(secret_string: str) -> int:
    """
    Converts the string to a sequence of hex values that is interpreted as an integer

    :param secret_string: str The secret string that must be encoded as a number
    :returns secret_number: int The secret string encoded
    :raises ValueError: If the character cannot be represented by two hex digits
    """

    Secret(secret_string)

    # Each single value character is given a leading 0 so they are all the same length
    # We start the string with '1' every time so if the first value has a leading 0 we do not lose any information
    encoded_secret = "1"

    for character in secret_string:

        # hex(18) gives 0x12 so [2:] discards the leading hex flag
        new_val = hex(ord(character))[2:]
        if len(new_val) < 2:
            new_val = "0" + new_val

        encoded_secret += new_val
    return int(encoded_secret, 16)


def integer_to_string(secret_number: int) -> str:
    """
    Converts the secret number to its string representation

    :param secret_number: int The secret string encoded
    :return: secret_string: str The secret string decoded from the number
    """
    if not isinstance(secret_number, int):
        raise TypeError("secret_number must be of type int")

    secret_string = ""
    # hex(18) gives 0x12 so [2:] discards the leading hex flag
    hex_number = hex(secret_number)[2:]

    for char_index in range(1, len(hex_number), 2):
        secret_string += chr(int(hex_number[char_index:char_index + 2], 16))

    return secret_string
