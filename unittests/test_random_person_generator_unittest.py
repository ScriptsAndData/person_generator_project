"""
Unit tests for the random_person_generator module.
"""
import unittest
from person_generator import random_person_generator as r

class TestRandomPerson(unittest.TestCase):
    """
    Test suite for functions within the random_person_generator module.
    """
    def test_select_sex(self):
        """Tests that select_sex returns either 'Male' or 'Female'."""
        self.assertIn(r.select_sex(), ["Male","Female"])

# This block allows the tests to be run directly from the command line,
# e.g., by executing 'python your_test_file.py'.
if __name__ == '__main__':
    unittest.main(argv=['ignored', '-v'], exit=False)
