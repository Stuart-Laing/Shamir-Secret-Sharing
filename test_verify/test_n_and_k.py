from shamir_secret_sharing_system.verify import NAndK

import unittest


class TestBase(unittest.TestCase):
    # Things to test
    # command_line_arg = True
    # 1   n = str(int) k = str(int) n == k
    # 1   n = str(int) k = str(int) n < k
    # 1   n = str(int) k = str(int) n > k
    # 3   n = str(-int) k = str(-int)
    # 4   n = str(float) k = str(float)
    # 5   n = str(-float) k = str(-float)
    # 6   n = str(str) k = str(str)

    # command_line_arg = False
    # 1   n = int k = int n == k
    # 1   n = int k = int n < k
    # 1   n = int k = int n > k
    # 3   n = -int k = -int

    # total_parts and min_for_reconstruct will always be int or str
    pass
