import shamir_secret_sharing_system
import unittest


class TestBase(unittest.TestCase):
    # Check if class accepts any object | shouldn't
    # Check if class accepts random strings when command line true | shouldn't
    # Check if class accepts random strings when command line false | shouldn't
    # Check if class accepts strings that are ints when command line true | should
    # Check if class accepts strings that are ints when command line false | shouldn't
    # Check if class accepts correct base | should
    # Check if class accepts incorrect base | shouldn't

    def test_allowed_base(self):
        # Any object being given as base
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base([1, 6, ""])
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base((0, "abc"))
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base(1.8)

        # Non int string being given as base when command_line_arg is true
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("wow that's neat", True)
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("10.235", True)
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("17 - 20", True)

        # Non int string being given as base when command_line_arg is false
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("wow that's real neat")
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("-29.1")
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("-24")

        # int string being given as base when command_line_arg is false
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("100")
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("-56")
        with self.assertRaises(TypeError):
            shamir_secret_sharing_system.verify.Base("16")

            # int string being given as base when command_line_arg is false
            with self.assertRaises(TypeError):
                shamir_secret_sharing_system.verify.Base("100")
            with self.assertRaises(TypeError):
                shamir_secret_sharing_system.verify.Base("-56")
            with self.assertRaises(TypeError):
                shamir_secret_sharing_system.verify.Base("16")


class TestFieldLimit(unittest.TestCase):
    pass


class TestNAndK(unittest.TestCase):
    pass


class TestNumber(unittest.TestCase):
    pass


class TestPartsFile(unittest.TestCase):
    pass


class TestSecret(unittest.TestCase):
    pass
