import shamir_secret_sharing_system
import random

from typing import Tuple


class _Polynomial:
    """
    Class to store the polynomial
    """
    def __init__(self, *values: int):
        """
        :param *values: int The values to build the polynomial
        """
        # TODO Find a better name than 'values'
        self.values: Tuple[int] = values

    def __repr__(self):
        output_string = " + ".join([f"{num}x^{index}" for index, num in enumerate(self.values)])

        return output_string

    def find_y(self, x: int, field_limit: int):
        """
        :param x: int The x value from which to find the y
        :param field_limit: int The field limit for the finite field arithmetic
        """
        y = 0
        for index, value in enumerate(self.values):
            exponentiation = (x ** index) % field_limit
            term = (value * exponentiation) % field_limit
            y = (y + term) % field_limit
        return y


def create_part_list(secret_number: int, total_parts_to_create: int, minimum_parts_for_reconstruction: int):
    """
    Creates a list of parts from the secret

    :param secret_number: int The secret in the form of a number to be split up
    :param total_parts_to_create: int The total number of parts that will be created
    :param minimum_parts_for_reconstruction: int The minimum amount of parts needed to get the secret back
    :returns parts: list A list of tuples containing the x and y values for the parts
    :returns field_limit: int The field limit used when computing the parts - needed for reconstruction
    """

    if not isinstance(secret_number, int):
        raise TypeError("secret_number must be of type int")
    if not isinstance(total_parts_to_create, int):
        raise TypeError("total_parts_to_create must be of type int")
    if not isinstance(minimum_parts_for_reconstruction, int):
        raise TypeError("minimum_parts_for_reconstruction must be of type int")

    shamir_secret_sharing_system.verify.NAndK(total_parts_to_create, minimum_parts_for_reconstruction)

    field_limit = 0
    for exponent in shamir_secret_sharing_system.constants.MERSENNE_PRIMES_EXPONENTS:
        if (2 ** exponent) - 1 > max(secret_number, total_parts_to_create):
            field_limit = (2 ** exponent) - 1
            break

    if field_limit == 0:
        pass
        # TODO Raise an error boi

    poly_numbers = set()
    while len(poly_numbers) != (minimum_parts_for_reconstruction - 1):
        poly_numbers.add(random.randint(2, field_limit - 1))

    secret_poly = _Polynomial(secret_number, *poly_numbers)

    parts = []
    for x_coord in range(1, total_parts_to_create + 1):
        parts.append((x_coord, secret_poly.find_y(x_coord, field_limit)))

    return parts, field_limit
