from shamir_secret_sharing_system.verify import Base
from shamir_secret_sharing_system.errors import BaseNotSupportedError

import unittest


# If command_line_arg is True then the input is a string 100%
# If command_line_arg is False then the input can be anything


class TestBase(unittest.TestCase):
    # Things to test
    # command_line_arg = True
    # 1   base = str(int)  valid base
    # 2   base = str(int)  invalid base
    # 3   base = str(-int)
    # 4   base = str(float)
    # 5   base = str(-float)
    # 6   base = str(str)

    # command_line_arg = False
    # 7   base = str(int)  valid base
    # 8   base = str(int)  invalid base
    # 9   base = str(-int)
    # 10  base = str(float)
    # 11  base = str(-float)
    # 12  base = str(str)
    # 13  base = int  valid base
    # 14  base = int  invalid base
    # 15  base = -int
    # 16  base = float
    # 17  base = -float
    # 18  base = str
    # 19  base = list
    # 20  base = tuple

    def test1(self):
        bases_to_test = (10, 16)
        for base in bases_to_test:
            try:
                Base(str(base), True)

            except TypeError:
                self.fail(f"Base({str(base)}, True) raised TypeError unexpectedly")

            except BaseNotSupportedError:
                self.fail(f"Base({str(base)}, True) raised BaseNotSupportedError unexpectedly")

    def test2(self):
        bases_to_test = (2, 99, 64)
        for base in bases_to_test:
            with self.assertRaises(BaseNotSupportedError):
                Base(str(base), True)

    def test3(self):
        bases_to_test = (-2, -16, -10)
        for base in bases_to_test:
            with self.assertRaises(BaseNotSupportedError):
                Base(str(base), True)

    def test4(self):
        bases_to_test = (2.11212, 16.7906, 1.631)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(str(base), True)

    def test5(self):
        bases_to_test = (-12.9, -40.1, -0.1)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(str(base), True)

    def test6(self):
        bases_to_test = ("wow that's amazing", "Wait, is it amazing?", "Nine-Nine!")
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(base, True)

    def test7(self):
        bases_to_test = (10, 16)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(str(base), False)

    def test8(self):
        bases_to_test = (11, 9, 64)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(str(base), False)

    def test9(self):
        bases_to_test = (-11, -9, -64)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(str(base), False)

    def test10(self):
        bases_to_test = (2.11212, 16.7906, 1.631)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(str(base), False)

    def test11(self):
        bases_to_test = (-2.11212, -16.7906, -1.631)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(str(base), False)

    def test12(self):
        bases_to_test = ("wow that's amazing", "Wait, is it amazing?", "Nine-Nine!")
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(base, False)

    def test13(self):
        bases_to_test = (10, 16)
        for base in bases_to_test:
            try:
                Base(base, False)

            except TypeError:
                self.fail(f"Base({base}, True) raised TypeError unexpectedly")

            except BaseNotSupportedError:
                self.fail(f"Base({base}, True) raised BaseNotSupportedError unexpectedly")

    def test14(self):
        bases_to_test = (2, 99, 64)
        for base in bases_to_test:
            with self.assertRaises(BaseNotSupportedError):
                Base(base, False)

    def test15(self):
        bases_to_test = (-2, -10, -16)
        for base in bases_to_test:
            with self.assertRaises(BaseNotSupportedError):
                Base(base, False)

    def test16(self):
        bases_to_test = (2.11212, 16.7906, 1.631)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(base, False)

    def test17(self):
        bases_to_test = (-12.9, -40.1, -0.1)
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(base, False)

    def test18(self):
        bases_to_test = ("wow that's amazing", "Wait, is it amazing?", "Nine-Nine!")
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(base, False)

    def test19(self):
        bases_to_test = ([], [1, 5], [0, 6])
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(base, False)

    def test20(self):
        bases_to_test = ((), (5, 10, 1), (1,))
        for base in bases_to_test:
            with self.assertRaises(TypeError):
                Base(base, False)
