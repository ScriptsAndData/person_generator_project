"""
Pytest suite for the random_person_generator module.

This module contains tests for functions that generate random person details
such as names, email, age, occupation, and phone numbers.
"""
import textwrap
import re
from unittest.mock import mock_open # mock_open still useful, even with pytest-mock

# For pytest-mock's mocker fixture (you need to 'pip install pytest-mock')
from pytest_mock import MockerFixture

from person_generator import random_person_generator as r

# Helper for patch targets (same as you used, works great here)
RPG = f"{r.__name__}"

class TestRandomPerson: # No inheritance from unittest.TestCase
    """
    Test suite for functions within the random_person_generator module using pytest.
    """
    def test_select_sex(self):
        """Tests that select_sex returns either 'Male' or 'Female'."""
        assert r.select_sex() in ["Male", "Female"]

    def test_select_random_name_from_file(self, mocker: MockerFixture): # Use mocker fixture
        """
        Tests that select_random_name_from_file correctly reads, parses,
        and selects a name from a mocked file.
        """
        fake_file_data = textwrap.dedent("""\
            MOCKJAMES     3.318  3.318       1
            MOCKJOHN      3.271  6.589       2
            MOCKROBERT    3.143  9.732       3
        """)

        # Using mocker.patch instead of unittest.mock.patch directly
        mock_file = mocker.patch("builtins.open", mock_open(read_data=fake_file_data))
        mock_choice = mocker.patch(f"{RPG}.choice", return_value="mockjohn")

        assert r.select_random_name_from_file("dummy_path.txt") == "Mockjohn"

        mock_file.assert_called_once_with("dummy_path.txt", "r", encoding='utf-8')
        mock_choice.assert_called_once_with(["MOCKJAMES", "MOCKJOHN", "MOCKROBERT"])

    def test_generate_first_name_male(self, mocker: MockerFixture):
        """
        Tests that generate_first_name returns a male name 
        by mocking the underlying name selection.
        """
        mock_core = mocker.patch(f"{RPG}.select_random_name_from_file", return_value="MockMaleName")

        assert r.generate_first_name("Male") == "MockMaleName"
        mock_core.assert_called_once_with(r.GEN_MALE_PATH)

    def test_generate_first_name_female(self, mocker: MockerFixture):
        """
        Tests that generate_first_name returns a female name 
        by mocking the underlying name selection.
        """
        mock_core = mocker.patch(f"{RPG}.select_random_name_from_file", return_value="MockFemaleName")

        assert r.generate_first_name("Female") == "MockFemaleName"
        mock_core.assert_called_once_with(r.GEN_FEMALE_PATH)

    def test_generate_last_name_wrapper(self, mocker: MockerFixture):
        """
        Tests that generate_last_name correctly calls the underlying
        name selection with the surname path.
        """
        mock_core = mocker.patch(f"{RPG}.select_random_name_from_file", return_value="Mockname")
        assert r.generate_last_name() == "Mockname"
        mock_core.assert_called_once_with(r.SURNAME_PATH)


