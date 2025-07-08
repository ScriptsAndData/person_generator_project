"""
Unit tests for the random_person_generator module.
"""
import unittest
from unittest.mock import patch, mock_open
import textwrap
import re
from person_generator import random_person_generator as r

class TestRandomPerson(unittest.TestCase):
    """
    Test suite for functions within the random_person_generator module.
    """
    def test_select_sex(self):
        """Tests that select_sex returns either 'Male' or 'Female'."""
        self.assertIn(r.select_sex(), ["Male","Female"])

    def test_select_random_name_from_file(self):
        """
        Tests that select_random_name_from_file correctly reads, parses,
        and selects a name from a mocked file.
        """
        fake_file_data = textwrap.dedent("""\
            MOCKJAMES     3.318  3.318       1
            MOCKJOHN      3.271  6.589       2
            MOCKROBERT    3.143  9.732       3
        """)
        with patch("builtins.open", mock_open(read_data=fake_file_data)
                   ) as mock_file:
            patch_target = f"{r.__name__}.choice"
            with patch(patch_target, return_value="mockjohn") as mock_choice:
                self.assertEqual(r.select_random_name_from_file(
                                                "dummy_path.txt"), "Mockjohn")
                mock_file.assert_called_once_with(
                                    "dummy_path.txt", "r", encoding='utf-8')
                mock_choice.assert_called_once_with(
                                    ["MOCKJAMES", "MOCKJOHN", "MOCKROBERT"])


# This block allows the tests to be run directly from the command line,
# e.g., by executing 'python your_test_file.py'.
if __name__ == '__main__':
    unittest.main(argv=['ignored', '-v'], exit=False)
