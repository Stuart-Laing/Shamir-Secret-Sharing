from .verify import Base, PartsFile
from .conversions import base_converter
from ._fraction import Fraction

from typing import List, Tuple, Union


__all__ = ["read_parts_from_file", "retrieve_secret_number"]


def read_parts_from_file(file_path: str, base: int) -> List[Tuple[int, Union[int, str]]]:
    """
    Read the parts from a text file

    :param file_path: str The path to the parts file
    :param base: int The number base the parts file is in
    :returns parts_list: list A list of tuples containing the x and y values for the parts
    """
    Base(base)
    PartsFile(file_path, base)

    with open(file_path, "r") as parts_file:
        parts_list = [(int(x.strip().split(" ")[0]), base_converter(x.strip().split(" ")[1], base, 10))
                      for x in parts_file.readlines()]

    return parts_list


def retrieve_secret_number(parts_list: List[Tuple[int, Union[int, str]]], field_limit: int) -> int:
    """
    Reconstruct the secret number from a parts list and field limit

    :param parts_list: list A list of tuples containing the x and y values for the parts
    :param field_limit: int The field limit used when computing the parts - needed for reconstruction
    :returns secret_number: int The secret number reconstructed from the parts list
    """
    if not isinstance(parts_list, list):
        raise TypeError("parts_list must be of type list")
    if not isinstance(field_limit, int):
        raise TypeError("field_limit must be of type int")

    secret_number = 0

    min_parts_needed = len(parts_list)

    for part_index, part in enumerate(parts_list):
        lagrange_fraction = Fraction(1, 1)

        for i in range(1, min_parts_needed + 1):
            if (i - 1) == part_index:
                continue

            lagrange_fraction *= Fraction(0 - parts_list[i - 1][0], parts_list[part_index][0] - parts_list[i - 1][0])

        lagrange_number = lagrange_fraction.numerator * _mod_inverse(lagrange_fraction.denominator, field_limit)

        secret_number = (secret_number + part[1] * lagrange_number) % field_limit

    return secret_number


def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Shamelessly stolen from https://brilliant.org/wiki/extended-euclidean-algorithm/

    :param a: int
    :param b: int
    """
    x = 0
    y = 1
    u = 1
    v = 0

    while a != 0:
        q = b // a
        r = b % a

        m = x - u * q
        n = y - v * q

        b = a
        a = r
        x = u
        y = v
        u = m
        v = n
    gcd = b
    return x, y, gcd


def _mod_inverse(k: int, prime: int) -> int:
    """
    :param k: int
    :param prime: int
    """
    y = _extended_gcd(prime, k)[1]

    return y % prime
