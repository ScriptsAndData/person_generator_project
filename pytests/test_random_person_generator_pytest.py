"""
Pytest suite for the random_person_generator module.

This module contains tests for functions that generate random person details
such as names, email, age, occupation, and phone numbers.
"""

# # For pytest-mock's mocker fixture (you need to 'pip install pytest-mock')
# from pytest_mock import MockerFixture

from person_generator import random_person_generator as r

class TestRandomPerson: # No inheritance from unittest.TestCase
    """
    Test suite for functions within the random_person_generator module using pytest.
    """
    def test_select_sex(self):
        """Tests that select_sex returns either 'Male' or 'Female'."""
        assert r.select_sex() in ["Male", "Female"]
