

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


"""
fraction1 = Fraction(5, 2)
fraction2 = Fraction(2, 5)

result1 = fraction1 * fraction2
result2 = fraction1 * 2
result3 = fraction1 + fraction2
result4 = fraction2 + 10

print(type(result1), result1)  # Should print '<class '__main__.Fraction'> 10/10'
print(type(result2), result2)  # Should print '<class '__main__.Fraction'> 10/2'
print()
print(type(result3), result3)  # Should print '<class '__main__.Fraction'> 29/10'
print(type(result4), result4)  # Should print '<class '__main__.Fraction'> 52/5'

print(Fraction(10, 4, reduce=True))
print(int(Fraction(20, 10, reduce=True)))
"""

parts = [(1, 9285275391624), (2, 27078320587385), (4, 87287720390361)]
required_parts = len(parts)

answer_parts = []

for index, part in enumerate(parts):
    answer_parts.append(None)
    for fraction in range(0, required_parts):
        if fraction != index:
            if answer_parts[index] is None:
                answer_parts[index] = Fraction(0 - parts[fraction][0], parts[index][0] - parts[fraction][0])

            else:
                answer_parts[index] *= Fraction(0 - parts[fraction][0], parts[index][0] - parts[fraction][0])


print(answer_parts)
print(Fraction(1, 3) * (0 - 2) * (0 - 4))

answer_parts[0] *= 9285275391624
answer_parts[1] *= 27078320587385
answer_parts[2] *= 87287720390361

slow_track_answer = answer_parts[0]
for fraction in answer_parts[1:]:
    slow_track_answer += fraction
print(slow_track_answer)

fast_track_answer = Fraction(9285275391624, 3) * (0 - 2) * (0 - 4) + \
                    Fraction(-27078320587385, 2) * (0 - 1) * (0 - 4) + \
                    Fraction(87287720390361, 6) * (0 - 1) * (0 - 2)

print()
print(fast_track_answer)
print(int(fast_track_answer + 91994388364979))
