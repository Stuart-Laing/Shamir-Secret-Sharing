import conversions


class Fraction:
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
            return Fraction(self.numerator * other, self.denominator, reduce=True)

        elif isinstance(other, Fraction):
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator, reduce=True)

        else:
            raise TypeError(f"Fraction Cannot be multiplied by {type(other)}")

    def __add__(self, other):
        if isinstance(other, int):
            return Fraction(self.numerator + (other * self.denominator), self.denominator, reduce=True)

        elif isinstance(other, Fraction):
            if self.denominator == other.denominator:
                return Fraction(self.numerator + other.numerator, self.denominator, reduce=True)

            new_denominator = self.denominator * other.denominator

            new_numerator1 = self.numerator * other.denominator
            new_numerator2 = other.numerator * self.denominator

            return Fraction(new_numerator1 + new_numerator2, new_denominator, reduce=True)

        else:
            raise TypeError(f"Fraction Cannot be added to by {type(other)}")

    def __sub__(self, other):
        if isinstance(other, int):
            return Fraction(self.numerator - (other * self.denominator), self.denominator, reduce=True)

        elif isinstance(other, Fraction):
            if self.denominator == other.denominator:
                return Fraction(self.numerator - other.numerator, self.denominator, reduce=True)

            new_denominator = self.denominator * other.denominator

            new_numerator1 = self.numerator * other.denominator
            new_numerator2 = other.numerator * self.denominator

            return Fraction(new_numerator1 - new_numerator2, new_denominator, reduce=True)

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


def read_parts_from_file(file_path):
    with open(file_path, "r") as parts_file:
        parts_list = [(int(x.strip().split(" ")[0]), int(x.strip().split(" ")[1])) for x in parts_file.readlines()]

    return parts_list


def extended_gcd(a, b):
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


def mod_inverse(k, prime):
    y = extended_gcd(prime, k)[1]

    return y % prime


def retrieve_secret(parts_list, field_limit):
    secret_number = 0

    min_parts_needed = len(parts_list)

    for part_index, part in enumerate(parts_list):
        lagrange_fraction = Fraction(1, 1)

        for i in range(1, min_parts_needed + 1):
            if (i - 1) == part_index:
                continue

            lagrange_fraction *= Fraction(0 - parts_list[i - 1][0], parts_list[part_index][0] - parts_list[i - 1][0])

        lagrange_number = lagrange_fraction.numerator * mod_inverse(lagrange_fraction.denominator, field_limit)

        secret_number = (secret_number + part[1] * lagrange_number) % field_limit

    return conversions.decode(secret_number)
