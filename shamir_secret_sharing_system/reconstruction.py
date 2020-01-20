import shamir_secret_sharing_system


class _Fraction:
    def __init__(self, numerator, denominator, reduce=False):
        if not (isinstance(numerator, int) and isinstance(denominator, int)):
            raise TypeError("Fraction numerator and denominator must be integers")
        if not isinstance(reduce, bool):
            raise TypeError("reduce must be boolean value")

        if numerator == 0 or denominator == 0:
            self.numerator = 0
            self.denominator = 0

        else:
            if (numerator < 0 and denominator < 0) or denominator < 0:
                self.numerator = numerator * -1
                self.denominator = denominator * -1
            else:
                self.numerator = numerator
                self.denominator = denominator

            if reduce:
                self.reduce()

    def __repr__(self):
        return f"{self.numerator}/{self.denominator}"

    def __mul__(self, other):
        if isinstance(other, int):
            return _Fraction(self.numerator * other, self.denominator, reduce=True)

        elif isinstance(other, _Fraction):
            return _Fraction(self.numerator * other.numerator, self.denominator * other.denominator, reduce=True)

        else:
            raise TypeError(f"Fraction Cannot be multiplied by {type(other)}")

    def __add__(self, other):
        if isinstance(other, int):
            return _Fraction(self.numerator + (other * self.denominator), self.denominator, reduce=True)

        elif isinstance(other, _Fraction):
            if self.denominator == other.denominator:
                return _Fraction(self.numerator + other.numerator, self.denominator, reduce=True)

            new_denominator = self.denominator * other.denominator

            new_numerator1 = self.numerator * other.denominator
            new_numerator2 = other.numerator * self.denominator

            return _Fraction(new_numerator1 + new_numerator2, new_denominator, reduce=True)

        else:
            raise TypeError(f"Fraction Cannot be added to by {type(other)}")

    def __sub__(self, other):
        if isinstance(other, int):
            return _Fraction(self.numerator - (other * self.denominator), self.denominator, reduce=True)

        elif isinstance(other, _Fraction):
            if self.denominator == other.denominator:
                return _Fraction(self.numerator - other.numerator, self.denominator, reduce=True)

            new_denominator = self.denominator * other.denominator

            new_numerator1 = self.numerator * other.denominator
            new_numerator2 = other.numerator * self.denominator

            return _Fraction(new_numerator1 - new_numerator2, new_denominator, reduce=True)

        else:
            raise TypeError(f"Fraction Cannot be subtracted by {type(other)}")

    def __int__(self):
        self.reduce()

        if self.denominator != 1:
            raise ValueError("Can't convert a fraction to int when the denominator is not 1")

        return self.numerator

    def reduce(self):
        if self.numerator % self.denominator == 0:
            self.numerator //= self.denominator
            self.denominator = 1
        else:
            for poss_factor in range(2, (min((self.numerator, self.denominator)) // 2) + 5):
                if self.numerator % poss_factor == 0 and self.denominator % poss_factor == 0:
                    self.numerator //= poss_factor
                    self.denominator //= poss_factor
                    break


def read_parts_from_file(file_path, base):
    """
    Read the parts from a text file

    :param file_path: str The path to the parts file
    :param base: int The number base the parts file is in
    :returns parts_list: list A list of tuples containing the x and y values for the parts
    """
    testing.verify.Base(base)
    testing.verify.PartsFile(file_path, base)

    with open(file_path, "r") as parts_file:
        parts_list = [(int(x.strip().split(" ")[0]),
                       shamir_secret_sharing_system.conversions.base_converter(x.strip().split(" ")[1], base, 10))
                      for x in parts_file.readlines()]

    return parts_list


def retrieve_secret_number(parts_list, field_limit):
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
        lagrange_fraction = _Fraction(1, 1)

        for i in range(1, min_parts_needed + 1):
            if (i - 1) == part_index:
                continue

            lagrange_fraction *= _Fraction(0 - parts_list[i - 1][0], parts_list[part_index][0] - parts_list[i - 1][0])

        lagrange_number = lagrange_fraction.numerator * _mod_inverse(lagrange_fraction.denominator, field_limit)

        secret_number = (secret_number + part[1] * lagrange_number) % field_limit

    return secret_number


def _extended_gcd(a, b):
    """
    Shamelessly stolen from https://brilliant.org/wiki/extended-euclidean-algorithm/
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


def _mod_inverse(k, prime):
    y = _extended_gcd(prime, k)[1]

    return y % prime
