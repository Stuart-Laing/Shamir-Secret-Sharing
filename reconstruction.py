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


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inverse(k, prime):
    k = k % prime
    if k < 0:
        r = egcd(prime, -k)[2]
    else:
        r = egcd(prime, k)[2]
    return (prime + r) % prime


def modular_lagrange_interpolation(x, points, prime):
    # break the points up into lists of x and y values
    x_values, y_values = zip(*points)
    # initialize f(x) and begin the calculation: f(x) = SUM( y_i * l_i(x) )
    f_x = 0
    for i in range(len(points)):
        # evaluate the lagrange basis polynomial l_i(x)
        numerator, denominator = 1, 1
        for j in range(len(points)):
            # don't compute a polynomial fraction if i equals j
            if i == j:
                continue
            # compute a fraction & update the existing numerator + denominator
            numerator = (numerator * (x - x_values[j])) % prime
            denominator = (denominator * (x_values[i] - x_values[j])) % prime
        # get the polynomial from the numerator + denominator mod inverse
        lagrange_polynomial = numerator * mod_inverse(denominator, prime)
        # multiply the current y & the evaluated polynomial & add it to f(x)
        f_x = (prime + f_x + (y_values[i] * lagrange_polynomial)) % prime
    return f_x


def retrieve_secret(parts_list, field_limit):

    return conversions.decode(modular_lagrange_interpolation(0, parts_list, field_limit))

    required_parts = len(parts_list)

    answer_parts = []

    # ################### BROKEN PART ###################
    for index, part in enumerate(parts_list):
        answer_parts.append(None)
        for fraction in range(0, required_parts):
            if fraction != index:
                if answer_parts[index] is None:
                    answer_parts[index] = \
                        Fraction(0 - parts_list[fraction][0], parts_list[index][0] - parts_list[fraction][0])

                else:
                    answer_parts[index] *= \
                        Fraction(0 - parts_list[fraction][0], parts_list[index][0] - parts_list[fraction][0])

    for part_index in range(0, len(parts_list)):
        answer_parts[part_index] *= parts_list[part_index][1]
    # ################### BROKEN PART ###################

    slow_track_answer = answer_parts[0]
    for fraction in answer_parts[1:]:
        slow_track_answer += fraction

    # print()
    # print(f"Fraction representation : {slow_track_answer}")

    return conversions.decode(int(slow_track_answer) % field_limit)
