# pytests/test_random_person_generator_pytest.py
"""
Pytest suite for the random_person_generator module.

This module contains tests for functions that generate random person details
such as names, email, age, occupation, and phone numbers.
"""
import re
import textwrap
from unittest.mock import mock_open

import pytest
from pytest_mock import MockerFixture

from person_generator import random_person_generator as r

# Helper for patch targets (same as you used, works great here)
RPG = f"{r.__name__}"

BORDER = "-----------------------------------"

MOCK_PERSON_DICT = {
                    "first_name": "MockFirst",
                    "last_name": "MockLast",
                    "sex": "Male",
                    "email": "mockfirst.mocklast@example.com",
                    "age": 30,
                    "job": "Programmer",
                    "phone_num": "03125 473 263",
                }

MOCK_JOB_FILE_DATA = textwrap.dedent("""\
            MOCKDOCTOR
            MOCKNURSE
            MOCKSURGEON
        """)

MOCK_INTERACTIVE_PARAMS = ("Male", 20, 70)

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
        mock_name_file_data = textwrap.dedent("""\
            MOCKJAMES     3.318  3.318       1
            MOCKJOHN      3.271  6.589       2
            MOCKROBERT    3.143  9.732       3
        """)

        # Using mocker.patch instead of unittest.mock.patch directly
        mock_open_file = mocker.patch("builtins.open", mock_open(read_data=mock_name_file_data))
        mock_choice = mocker.patch(f"{RPG}.choice", return_value="mockjohn")

        assert r.select_random_name_from_file("dummy_path.txt") == "Mockjohn"

        mock_open_file.assert_called_once_with("dummy_path.txt", "r", encoding='utf-8')
        mock_choice.assert_called_once_with(["MOCKJAMES", "MOCKJOHN", "MOCKROBERT"])


    @pytest.mark.parametrize(
        "gender_input, name_type_input, mock_return_value, expected_file_path, expected_output",
        [
            (
                "Male",            # Male gender_input
                "first",           # first name_type_input
                "MockMaleName",    # return_value for the mocked select_random_name_from_file
                r.GEN_MALE_PATH,   # expected argument for select_random_name_from_file
                "MockMaleName"     # expected output of generate_name
            ),
            (
                "Female",          # Female
                "first",           # first name
                "MockFemaleName",
                r.GEN_FEMALE_PATH,
                "MockFemaleName"
            ),
            (
                "",                # non-specified gender
                "last",            # last name
                "MockSurname",
                r.SURNAME_PATH,
                "MockSurname"
            )
        ]
    )
    def test_generate_name(
        self,
        mocker: MockerFixture,
        name_type_input: str,
        gender_input: str,
        mock_return_value: str,
        expected_file_path,
        expected_output: str
    ):
        """
        Tests that generate_name returns the correct name based on gender,
        by mocking the underlying name selection and verifying file path.
        """
        # Mock the direct dependency: select_random_name_from_file
        mock_core = mocker.patch(
            f"{RPG}.select_random_name_from_file",
            return_value=mock_return_value
        )

        # Call the function being tested
        actual_output = r.generate_name(name_type_input, gender_input)

        # Assert the function returns the expected output
        assert actual_output == expected_output

        # Assert the mock was called correctly with the expected file path
        mock_core.assert_called_once_with(expected_file_path)


    def test_generate_email(self):
        """
        Tests generate_email with known input, verifies format, and asserts provider.
        """
        first = "MockFirst"
        last = "MockLast"

        generated_email = r.generate_email(first, last)

        assert '@' in generated_email
        assert generated_email.endswith('.com')

        match = re.match(r"([a-z]+)\.([a-z]+)@([a-z]+)\.com", generated_email)
        assert match is not None, (
            f"Email format '{generated_email}' did not match expected pattern.")

        extracted_first = match.group(1)
        extracted_last = match.group(2)
        extracted_provider = match.group(3)

        assert extracted_first == first.lower()
        assert extracted_last == last.lower()

        expected_providers = ["aol", "gmail", "outlook", "yahoo", "icloud", "yandex"]
        assert extracted_provider in expected_providers

    def test_generate_age(self):
        """
        Tests that generate_age returns an integer within the expected range (1 to 100).
        """
        age = r.generate_age()
        assert age >= 1
        assert age <= 100

    def test_generate_phone_num(self):
        """
        Tests that generate_phone_num returns a string matching the expected phone format.
        """
        phone_pattern = r"^\d{5} \d{3} \d{3}$"
        phone_num = r.generate_phone_num()
        assert re.match(phone_pattern, phone_num) is not None, \
            f"Phone number '{phone_num}' does not match expected format '{phone_pattern}'"
        assert isinstance(phone_num, str)

    @pytest.mark.parametrize(
        "file_data, expected_parsed_list, mock_choice_return, expected_output",
        [
            (MOCK_JOB_FILE_DATA,
             ["MOCKDOCTOR", "MOCKNURSE", "MOCKSURGEON"], "mockdoctor", "Mockdoctor"),
            (textwrap.dedent("SINGLEJOB"), ["SINGLEJOB"], "singlejob", "Singlejob"),
            ("", [], "", "") # Test empty file scenario
        ]
    )
    def test_select_random_job_from_file_parametrized(
        self, mocker, file_data, expected_parsed_list, mock_choice_return, expected_output
    ):
        mock_file = mocker.patch("builtins.open", mock_open(read_data=file_data))
        mock_choice = mocker.patch(f"{RPG}.choice", return_value=mock_choice_return)

        assert r.select_random_job_from_file("dummy_path.txt") == expected_output
        mock_file.assert_called_once_with("dummy_path.txt", "r", encoding='utf-8')
        mock_choice.assert_called_once_with(expected_parsed_list)


    def test_generate_occupation(self, mocker: MockerFixture):
        """
        Tests key aspects of the generate_occupation function with two asserts.
        """
        mock_core = mocker.patch(f"{RPG}.select_random_job_from_file", return_value="MockJob")
        assert r.generate_occupation(5) == "Child"
        assert r.generate_occupation(30) == "MockJob"
        assert r.generate_occupation(80) == "Retired"
        mock_core.assert_called_once_with(r.JOBS_PATH)

    def test_generate_person_details_dict(self, mocker: MockerFixture):
        """
        Tests generate_random_person_details_dict by mocking all its dependencies
        and asserting the final dictionary content.
        """
        # Patching with mocker.patch (no decorators needed)
        mock_select_sex = mocker.patch(f"{RPG}.select_sex", return_value="Male")
        mock_generate_name = mocker.patch(
            f"{RPG}.generate_name",
            side_effect=["MockFirst", "MockLast"])
        mock_generate_email = mocker.patch(
            f"{RPG}.generate_email", return_value="mockfirst.mocklast@example.com")
        mock_generate_age = mocker.patch(f"{RPG}.generate_age", return_value=30)
        mock_generate_occupation = mocker.patch(
            f"{RPG}.generate_occupation", return_value="Programmer")
        mock_generate_phone_num = mocker.patch(
            f"{RPG}.generate_phone_num", return_value="03125 473 263")

        generated_dict = r.generate_person_dict("",0,0)
        expected_dict = MOCK_PERSON_DICT
        assert generated_dict == expected_dict

        # Assert calls (no change needed here for assert_called_once_with)
        mock_select_sex.assert_called_once()

        mock_generate_name.assert_has_calls(
            [mocker.call("first", "Male"), mocker.call("last")] ) # type: ignore
        assert mock_generate_name.call_count == 2

        mock_generate_email.assert_called_once_with("MockFirst", "MockLast")
        mock_generate_age.assert_called_once()
        mock_generate_occupation.assert_called_once_with(30)
        mock_generate_phone_num.assert_called_once()


    @pytest.mark.parametrize(
        "input_person_dict, expected_data_lines, expected_num_lines",
        [
            # Test Case 1: Standard person data
            (
                MOCK_PERSON_DICT,
                [
                    ("first_name", "MockFirst"),
                    ("last_name", "MockLast"),
                    ("sex", "Male"),
                    ("email", "mockfirst.mocklast@example.com"),
                    ("age", "30"), # Age might be formatted as string in output
                    ("job", "Programmer"),
                    ("phone_num", "03125 473 263"),
                ],
                11, # 3 header lines + 7 data lines + 1 end line = 11
            ),
            # Test Case 2: A person with fewer details (example of testing variation)
            (
                {
                    "first_name": MOCK_PERSON_DICT["first_name"],
                    "age": MOCK_PERSON_DICT["age"],
                },
                [
                    ("first_name", MOCK_PERSON_DICT["first_name"]),
                    ("age", MOCK_PERSON_DICT["age"]),
                ],
                6, # 3 header lines + 2 data lines + 1 end line = 6
            ),
            # Test Case 3: Empty person dictionary (if your function handles this gracefully)
            (
                {},
                [], # No data lines expected
                4, # 3 header lines + 0 data lines + 1 end line = 4
            )
        ]
    )
    def test_format_person_for_display(
        self, input_person_dict, expected_data_lines, expected_num_lines):
        """
        Tests the format_person_for_display function's output structure and content
        using parametrization for different person data.
        """
        actual_output = r.format_person_for_display(input_person_dict)
        lines = actual_output.splitlines()

        # 1 Test Header and Footer
        assert lines[0] == BORDER
        assert lines[1].strip() == "PERSON DETAILS"
        assert lines[2] == BORDER
        assert lines[-1] == BORDER

        # 2 Check display of actual data lines
        actual_data_lines = lines[3:-1] # From index 3 up to, but not including, the last line
        assert len(actual_data_lines) == len(expected_data_lines), (
            f"Expected {len(expected_data_lines)} data lines, got {len(actual_data_lines)}")

        for i, (key, value) in enumerate(expected_data_lines):
            expected_substring = f"{key:<15}: {value}" # Example, adjust based on actual spacing
            # Use regex or more flexible string checking if spacing varies wildly
            assert expected_substring in actual_data_lines[i], (
                f"Line {i+3}: Expected '{expected_substring}' but found '{actual_data_lines[i]}'")

        # 3. Overall structural check - total number of lines
        assert len(lines) == expected_num_lines, (
            f"Expected {expected_num_lines} total lines, got {len(lines)}")


    @pytest.mark.parametrize(
        "mock_inputs, expected_outputs",
        [
            (("male", "11", "81"),   ("male", 11, 81)),
            (("female", "25", "61"), ("female", 25, 61)),
            (("", "", ""),           ("random", 10, 85)),
            (("random", "", ""),     ("random", 10, 85))
        ]
    )
    def test_get_interactive_person_parameters(self, mocker, mock_inputs, expected_outputs):
        mocker.patch('builtins.input', side_effect=mock_inputs)
        assert r._get_interactive_person_parameters() == expected_outputs


    # def test_main(self):
    #     assert r.main() == expected_person_dict
