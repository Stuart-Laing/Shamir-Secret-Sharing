from shamir_secret_sharing_system.fraction import Fraction
import unittest


# TODO
# Test if repr works
# Test if eq works | Fraction == Fraction | Fraction == other
# Test if multiply works | Fraction * Fraction | Fraction * int | Fraction * other
# Test if divide works | Fraction / Fraction - Fraction / int | Fraction / other
# Test if add works | Fraction + Fraction | Fraction + int | Fraction + other
# Test if sub works | Fraction - Fraction | Fraction - int | Fraction - other
# Test if int works | Not 1 denominator | Yes 1 denominator
# Test if reduce works
# ADD MESSAGES


class TestFraction(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Fraction(1, 2)), "1/2")
        self.assertEqual(repr(Fraction(5, 2)), "5/2")
        self.assertEqual(repr(Fraction(54, 20)), "54/20")

    def test_eq(self):
        self.assertTrue(Fraction(1, 2) == Fraction(1, 2))
        self.assertTrue(Fraction(10, 1) == Fraction(100, 10))
        self.assertTrue(Fraction(1, 5) == Fraction(5, 25))

        self.assertFalse(Fraction(30, 1) == Fraction(52, 12))
        self.assertFalse(Fraction(3, 10) == Fraction(5, 7))
        self.assertFalse(Fraction(4, 22) == Fraction(99, 100))

        with self.assertRaises(TypeError):
            _ = Fraction(12, 5) == 20
            _ = Fraction(97, 102) == "Nope"
            _ = Fraction(2, 21445) == [1, 6, 2]

    def test_multiply(self):
        self.assertEqual(Fraction(2, 3) * Fraction(1, 3), Fraction(2, 9))
        self.assertEqual(Fraction(10, 20) * Fraction(20, 10), Fraction(1, 1))
        self.assertEqual(Fraction(20, 21) * Fraction(2, 2), Fraction(20, 21))

        self.assertEqual(Fraction(5, 2) * 2, Fraction(5, 1))
        self.assertEqual(Fraction(3, 2) * 10, Fraction(15, 1))
        self.assertEqual(Fraction(9, 10) * 43, Fraction(387, 10))

        with self.assertRaises(TypeError):
            _ = Fraction(50, 51) * "Wow thats amazing"
            _ = Fraction(1, 2) * 10.123
            _ = Fraction(9, 1) * [1, 5]

    def test_truediv(self):
        self.assertEqual(Fraction(2, 3) / Fraction(1, 3), Fraction(2, 1))
        self.assertEqual(Fraction(10, 20) / Fraction(20, 10), Fraction(1, 4))
        self.assertEqual(Fraction(20, 21) / Fraction(2, 2), Fraction(20, 21))

        self.assertEqual(Fraction(5, 2) / 2, Fraction(5, 4))
        self.assertEqual(Fraction(3, 2) / 10, Fraction(3, 20))
        self.assertEqual(Fraction(9, 10) / 43, Fraction(9, 430))

        with self.assertRaises(TypeError):
            _ = Fraction(50, 51) / "Wow thats amazing"
            _ = Fraction(1, 2) / 10.123
            _ = Fraction(9, 1) / [1, 5]

    def test_add(self):
        self.assertEqual(Fraction(2, 3) + Fraction(1, 3), Fraction(1, 1))
        self.assertEqual(Fraction(10, 20) + Fraction(20, 10), Fraction(5, 2))
        self.assertEqual(Fraction(20, 21) + Fraction(2, 2), Fraction(41, 21))

        self.assertEqual(Fraction(5, 2) + 2, Fraction(9, 2))
        self.assertEqual(Fraction(3, 2) + 10, Fraction(23, 2))
        self.assertEqual(Fraction(9, 10) + 43, Fraction(439, 10))

        with self.assertRaises(TypeError):
            _ = Fraction(50, 51) + "Wow thats amazing"
            _ = Fraction(1, 2) + 10.123
            _ = Fraction(9, 1) + [1, 5]

    def test_sub(self):
        self.assertEqual(Fraction(2, 3) - Fraction(1, 3), Fraction(1, 3))
        self.assertEqual(Fraction(10, 20) - Fraction(20, 10), Fraction(-3, 2))
        self.assertEqual(Fraction(20, 21) - Fraction(2, 2), Fraction(-1, 21))

        self.assertEqual(Fraction(5, 2) - 2, Fraction(1, 2))
        self.assertEqual(Fraction(3, 2) - 10, Fraction(-17, 2))
        self.assertEqual(Fraction(9, 10) - 43, Fraction(-421, 10))

        with self.assertRaises(TypeError):
            _ = Fraction(50, 51) - "Wow thats amazing"
            _ = Fraction(1, 2) - 10.123
            _ = Fraction(9, 1) - [1, 5]

    def test_int(self):
        self.assertEqual(int(Fraction(32, 1)), 32)
        self.assertEqual(int(Fraction(-24, 2)), -12)
        self.assertEqual(int(Fraction(66, 2)), 33)

        with self.assertRaises(ValueError):
            _ = int(Fraction(-5, 51))
            _ = int(Fraction(123, 50))
            _ = int(Fraction(5, 10))

    def test_reduce(self):
        self.assertEqual(Fraction(20, 10, reduce=True), Fraction(2, 1))
        self.assertEqual(Fraction(12000000, 52000000, reduce=True), Fraction(3, 13))
        self.assertEqual(Fraction(52, 12, reduce=True), Fraction(13, 3))
