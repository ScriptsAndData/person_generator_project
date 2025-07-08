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

    def test_generate_first_name_male(self):
        """
        Tests that generate_first_name returns a mock male name 
        by mocking the underlying name selection.
        """
        patch_target = f"{r.__name__}.select_random_name_from_file"
        with patch(patch_target, return_value="MockMaleName") as mock_core:
            self.assertEqual(r.generate_first_name("Male"), "MockMaleName")
            mock_core.assert_called_once_with(r.GEN_MALE_PATH)

    def test_generate_first_name_female(self):
        """
        Tests that generate_first_name returns a mock female name 
        by mocking the underlying name selection.
        """
        patch_target = f"{r.__name__}.select_random_name_from_file"
        with patch(patch_target, return_value="MockFemaleName") as mock_core:
            self.assertEqual(r.generate_first_name("Female"), "MockFemaleName")
            mock_core.assert_called_once_with(r.GEN_FEMALE_PATH)

    def test_generate_last_name_wrapper(self):
        """
        Tests that generate_last_name correctly calls the underlying
        name selection with the surname path.
        """
        patch_target = f"{r.__name__}.select_random_name_from_file"
        with patch(patch_target, return_value="Mockname") as mock_core:
            self.assertEqual(r.generate_last_name(), "Mockname")
            mock_core.assert_called_once_with(r.SURNAME_PATH)

# This block allows the tests to be run directly from the command line,
# e.g., by executing 'python your_test_file.py'.
if __name__ == '__main__':
    unittest.main(argv=['ignored', '-v'], exit=False)
