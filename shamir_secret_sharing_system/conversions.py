

def string_to_integer(secret_string):
    """
    Converts the string to a sequence of hex values that is interpreted as an integer

    :param secret_string: str The secret string that must be encoded as a number
    :returns secret_number: int The secret string encoded
    :raises ValueError: If the character cannot be represented by two hex digits
    """
    # Each single value character is given a leading 0 so they are all the same length
    # We start the string with '1' every time so if the first value has a leading 0 we do not lose any information
    encoded_secret = "1"

    for character in secret_string:
        if ord(character) > 255:
            raise ValueError("All characters must be able to be represented by two hex digits")

        # hex(18) gives 0x12 so [2:] discards the leading hex flag
        new_val = hex(ord(character))[2:]
        if len(new_val) < 2:
            new_val = "0" + new_val

        encoded_secret += new_val
    return int(encoded_secret, 16)


def integer_to_string(secret_number):
    """
    Converts the secret number to its string representation

    :param secret_number: int The secret string encoded
    :return: secret_string: str The secret string decoded from the number
    """
    secret_string = ""
    # hex(18) gives 0x12 so [2:] discards the leading hex flag
    hex_number = hex(secret_number)[2:]

    for char_index in range(1, len(hex_number), 2):
        secret_string += chr(int(hex_number[char_index:char_index + 2], 16))

    return secret_string
