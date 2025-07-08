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

    def test_generate_email(self):
        """
        Tests generate_email with known input, verifies format, and asserts provider.
        """
        first = "MockFirst"
        last = "MockLast"

        # Call the function under test (allowing random.choice to pick a real provider)
        generated_email = r.generate_email(first, last)

        # 1. Verify the format of the email address with '@' and .com
        self.assertIn('@', generated_email, "Email should contain '@'")
        self.assertTrue(generated_email.endswith('.com'), "Email should end with '.com'")

        # Use regex to extract parts: (first_name).(last_name)@(provider).com
        match = re.match(r"([a-z]+)\.([a-z]+)@([a-z]+)\.com", generated_email)
        self.assertIsNotNone(match, f"Email format '{generated_email}' "
                             "did not match expected pattern.")

        extracted_first = match.group(1)
        extracted_last = match.group(2)
        extracted_provider = match.group(3)

        # 2. Extract first name and last name and assertEqual on each of them
        self.assertEqual(extracted_first, first.lower(),"Extracted first name "
            f"'{extracted_first}' does not match expected '{first.lower()}'")
        self.assertEqual(extracted_last, last.lower(), "Extracted last name "
            f"'{extracted_last}' does not match expected '{last.lower()}'")

        # 3. Extract the returned provider and assertIn the list of providers
        expected_providers = ["aol", "gmail", "outlook", "yahoo", "icloud", "yandex"]
        self.assertIn(extracted_provider, expected_providers,
                      f"Extracted provider '{extracted_provider}' not in expected list.")

    def test_generate_age(self):
        """
        Tests that generate_age returns an integer within the expected range (1 to 100).
        """
        self.assertGreaterEqual(r.generate_age(),1,"Age lesser than 1")
        self.assertLessEqual(r.generate_age(),100,"Age greater than 100")

    def test_generate_phone_num(self):
        """
        Tests that generate_phone_num returns a string matching the expected phone format.
        """
        phone_pattern = r"^\d{5} \d{3} \d{3}$"
        phone_num = r.generate_phone_num()
        self.assertRegex(phone_num, phone_pattern,
          f"Phone number '{phone_num}' does not match expected format '{phone_pattern}'")
        self.assertIsInstance(phone_num, str) # Also check type

    def test_generate_occupation(self):
        """
        Tests key aspects of the generate_occupation function with two asserts.
        """
        # Assert 1: Adult job selection
        # Define the expected list of adult jobs, mirroring the function's internal list
        expected_adult_jobs = [
            "cook", "actor", "programmer", "doctor", "dentist",
            "uber driver", "photographer", "astronaut", "policeman"
        ]
        # Test with an age clearly in the adult range
        adult_age = 30
        occupation_adult = r.generate_occupation(adult_age)
        self.assertIn(occupation_adult, expected_adult_jobs,
                      f"Expected an adult job from {expected_adult_jobs} for age {adult_age}")

        # Assert 2: Child job selection
        # Test with an age clearly in the child range
        child_age = 5
        occupation_child = r.generate_occupation(child_age)
        self.assertEqual(occupation_child, "child",
                         f"Expected 'child' for age {child_age}")

# This block allows the tests to be run directly from the command line,
# e.g., by executing 'python your_test_file.py'.
if __name__ == '__main__':
    unittest.main(argv=['ignored', '-v'], exit=False)
