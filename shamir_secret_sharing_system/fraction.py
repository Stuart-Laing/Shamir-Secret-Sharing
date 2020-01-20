

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

    def __eq__(self, other):
        if isinstance(other, Fraction):
            fraction1 = Fraction(self.numerator, self.denominator, reduce=True)
            fraction2 = Fraction(other.numerator, other.denominator, reduce=True)

            return fraction1.numerator == fraction2.numerator and fraction1.denominator == fraction2.denominator
        else:
            raise TypeError(f"Cannot check equality between Fraction and {type(other)}")

    def __mul__(self, other):
        if isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator, reduce=True)

        elif isinstance(other, Fraction):
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator, reduce=True)

        else:
            raise TypeError(f"Fraction Cannot be multiplied by {type(other)}")

    def __truediv__(self, other):
        if isinstance(other, int):
            return self * Fraction(1, other, reduce=True)

        elif isinstance(other, Fraction):
            return self * Fraction(other.denominator, other.numerator, reduce=True)

        else:
            raise TypeError(f"Fraction Cannot be divided by {type(other)}")

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
        if self.numerator < 0:
            self.numerator *= -1
            was_negative = True
        else:
            was_negative = False

        if self.numerator % self.denominator == 0:
            self.numerator //= self.denominator
            self.denominator = 1
        else:
            divisor_found = False
            while True:
                for poss_factor in range(2, (min((self.numerator, self.denominator)) // 2) + 5):
                    if self.numerator % poss_factor == 0 and self.denominator % poss_factor == 0:
                        self.numerator //= poss_factor
                        self.denominator //= poss_factor
                        divisor_found = True
                        break
                if divisor_found:
                    divisor_found = False
                else:
                    break

        if was_negative:
            self.numerator *= -1
