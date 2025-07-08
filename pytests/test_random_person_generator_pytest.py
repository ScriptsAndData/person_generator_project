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
