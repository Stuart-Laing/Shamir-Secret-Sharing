from shamir_secret_sharing_system.verify import FieldLimit

import unittest


class TestBase(unittest.TestCase):
    # Things to test
    # base 10
    # 1   field_limit = Works for base
    # 2   field_limit = Doesn't work for base
    # base 16
    # 3   field_limit = Works for base
    # 4   field_limit = Doesn't work for base

    def test1(self):
        field_limits = ("18729160981234", "12345", "0")
        for field_limit in field_limits:
            try:
                FieldLimit(field_limit, 10)

            except ValueError:
                self.fail(f"FieldLimit({field_limit}, 10) raised ValueError unexpectedly")

    def test2(self):
        field_limits = ("18abcdeff4", "1FFF5", "FF")
        for field_limit in field_limits:
            with self.assertRaises(ValueError):
                FieldLimit(field_limit, 10)

    def test3(self):
        field_limits = ("18abcdeff4", "1FFF5", "0")
        for field_limit in field_limits:
            try:
                FieldLimit(field_limit, 16)

            except ValueError:
                self.fail(f"FieldLimit({field_limit}, 10) raised ValueError unexpectedly")

    def test4(self):
        field_limits = ("[p'lk;jhuigtoyur6tfgh", "AbfF-+", "cuuuuuuuuuuuup")
        for field_limit in field_limits:
            with self.assertRaises(ValueError):
                FieldLimit(field_limit, 16)
