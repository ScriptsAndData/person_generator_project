# pytests/test_random_person_generator_pytest.py
"""
Pytest suite for the random_person_generator module.

This module contains tests for functions that generate random person details
such as names, email, age, occupation, and phone numbers.
"""
import re
from typing import Any, Tuple, Callable
from pathlib import Path

import sys
from types import SimpleNamespace
from unittest.mock import mock_open, patch
import pytest
from pytest_mock import MockerFixture

from person_generator.random_person_generator import EMAIL_PROVIDERS
from person_generator.random_person_generator import DEFAULT_MAX_AGE
from person_generator.random_person_generator import DEFAULT_MIN_AGE
from person_generator import random_person_generator as r

from person_generator.display_formatters import BORDER

from .conftest import TEST_READ_FILE_VARIOUS_INPUTS_CASES
from .conftest import TEST_GENERATE_RANDOM_VALUE_FROM_FILE
from .conftest import TEST_DISPLAY_PEOPLE_CASES


class TestRandomPerson: # No inheritance from unittest.TestCase
    """
    Test suite for functions within the random_person_generator module using pytest.
    """
    def test_generate_sex(self) -> None:
        """Tests that generate_sex returns either 'Male' or 'Female'."""
        assert r.generate_sex() in ["Male", "Female"]


    def test_generate_age(self) -> None:
        """
        Tests that generate_age returns an integer within the expected range (1 to 100).
        """
        age = r.generate_age()
        assert age >= 1
        assert age <= 100
        assert isinstance(age, int)


    @pytest.mark.parametrize(
        "mock_file_content, file_path_arg, regex_pattern, transform_func, expected_outcome",
        TEST_READ_FILE_VARIOUS_INPUTS_CASES
    )
    # pylint: disable=R0917
    def test_read_files_various_inputs(
            self,
            mocker: MockerFixture,
            mock_file_content: str,
            file_path_arg: Path,
            regex_pattern: str,
            transform_func: Callable[[str], str],
            expected_outcome: Any, # Use Any if it can be a string or a pytest.raises context
    ) -> None:
        """
        Tests r.read_files_various_inputs for various file types and scenarios
        using a single-line mock and parametrization.
        """
        # 1. Arrange: Patch builtins.open to return our mock file content
        mock_open_func = mocker.patch("builtins.open", mock_open(read_data=mock_file_content))

        # 2. Act & Assert based on expected_outcome
        if isinstance(expected_outcome, type) and issubclass(expected_outcome, Exception):
            # This branch handles cases where an exception is expected
            # (e.g., IndexError for empty file)
            with pytest.raises(expected_outcome, match="No items were found from the file" \
            ""): # Adjust match as needed
                r.read_files_various_inputs(file_path_arg, regex_pattern, transform_func)
            mock_open_func.assert_called_once_with(file_path_arg, 'r', encoding='utf-8')
        else:
            # This branch handles cases where a successful string result is expected
            result = r.read_files_various_inputs(file_path_arg, regex_pattern, transform_func)
            assert result == expected_outcome
            mock_open_func.assert_called_once_with(file_path_arg, 'r', encoding='utf-8')


    @pytest.mark.parametrize(
        ("generator_func, generator_func_args, expected_path, expected_regex,"
        "expected_transform_func, mock_return_value, read_func_expected_to_be_called"),
        TEST_GENERATE_RANDOM_VALUE_FROM_FILE
    )
    # pylint: disable=R0917
    def test_generate_random_value_from_file(
        self,
        mocker: MockerFixture,
        generator_func: Callable[..., str],
        generator_func_args: Tuple[Any, ...],  # Tuple to handle 0 or more args
        expected_path: Path,
        expected_regex: str,
        expected_transform_func: Callable[[str], str],
        mock_return_value: str,
        read_func_expected_to_be_called: bool
    ) -> None:
        """
        Consolidated unit test for data generation functions (first name, last name, occupation).
        Ensures correct path selection, regex, and transform_func, and return value based on mocked
        read_files_various_inputs.
        """
        # Arrange: Mock the read_files_various_inputs function
        mock_read_func = mocker.patch(
            "person_generator.random_person_generator.read_files_various_inputs",
            return_value=mock_return_value # Define what our mock dependency returns
        )

        # Act: Call the function under test
        returned_generated_item = generator_func(*generator_func_args) # Unpack the tuple of args

        # Assert:
        # 1. Verify that generate_first_name returned the expected value
        assert returned_generated_item == mock_return_value

        # 2. Verify read_files_various_inputs was called
        # either once or not at all
        if read_func_expected_to_be_called:
            mock_read_func.assert_called_once()
            # 3. Verify that read_files_various_inputs was called with the CORRECT arguments
            # This is where we ensure the path selection logic is correct.
            mock_read_func.assert_called_once_with(
                expected_path,         # The path determined by gender
                expected_regex,        # The hardcoded regex
                expected_transform_func # The hardcoded transform function
            )
        else:
            mock_read_func.assert_not_called()


    def test_generate_email(self) -> None:
        """
        Tests generate_email with known input, verifies format, and asserts provider.
        """
        first = "MockFirst"
        last = "MockLast"

        generated_email = r.generate_email(first, last)

        match = re.match(r"([a-z]+)\.([a-z]+)@([a-z]+)\.com", generated_email)
        assert match is not None, (
            f"Email format '{generated_email}' did not match expected pattern.")

        extracted_first = match.group(1)
        extracted_last = match.group(2)
        extracted_provider = match.group(3)

        assert extracted_first == first.lower()
        assert extracted_last == last.lower()

        expected_providers = EMAIL_PROVIDERS
        assert extracted_provider in expected_providers


    def test_generate_phone_num(self) -> None:
        """
        Tests that generate_phone_num returns a string matching the expected phone format.
        """
        phone_pattern = r"^\(\d{3}\) \d{3}-\d{4}$"
        phone_num = r.generate_phone_num()
        assert re.match(phone_pattern, phone_num) is not None, \
            f"Phone number '{phone_num}' does not match expected format '{phone_pattern}'"
        assert isinstance(phone_num, str)


    def test_generate_person_dict(
        self,
        mocker: MockerFixture
    ) -> None:
        """
        Unit test for generate_person_dict function.
        It mocks all internal dependent calls and verifies:
        1. Correct arguments are passed to the mocks.
        2. The final dictionary is correctly composed from mock return values.
        """
        # Setup Mock call and return values
        gender_choice: str = "male"
        age_min: int = 18
        age_max: int = 80

        expected_person_dict = {
            "first_name": "Kory",
            "last_name": "Ahrns",
            "sex": "Male",
            "email": "kory.ahrns@fastmail.com",
            "age": 68,
            "job": "Retired",
            "phone_num": "(705) 385-7324"
        }
        # Define shortcut variable ex for expected_person_dict
        ex = expected_person_dict

        # --- Arrange: Mock all internal dependencies ---
        # Each mock is set to return a predefined value
        mock_generate_sex = mocker.patch(
            'person_generator.random_person_generator.generate_sex',
            return_value=ex["sex"]
        )
        mock_generate_first_name = mocker.patch(
            'person_generator.random_person_generator.generate_first_name',
            return_value=ex["first_name"]
        )
        mock_generate_last_name = mocker.patch(
            'person_generator.random_person_generator.generate_last_name',
            return_value=ex["last_name"]
        )
        mock_generate_email = mocker.patch(
            'person_generator.random_person_generator.generate_email',
            return_value=ex["email"]
        )
        mock_generate_age = mocker.patch(
            'person_generator.random_person_generator.generate_age',
            return_value=ex["age"]
        )
        mock_generate_occupation = mocker.patch(
            'person_generator.random_person_generator.generate_occupation',
            return_value=ex["job"]
        )
        mock_generate_phone_num = mocker.patch(
            'person_generator.random_person_generator.generate_phone_num',
            return_value=ex["phone_num"]
        )

        # --- Act: Call the function under test ---
        actual_person_dict = r.generate_person_dict(gender_choice, age_min, age_max)

        # --- Assert: Verify interactions and final result ---

        # 1. Verify that each mocked function was called exactly once with the correct arguments
        mock_generate_sex.assert_called_once_with(gender_choice)

        # Note: The arguments to subsequent mocks are the *return values* of previous mocks
        mock_generate_first_name.assert_called_once_with(ex["sex"])
        mock_generate_last_name.assert_called_once_with() # No arguments expected
        mock_generate_email.assert_called_once_with(ex["first_name"], ex["last_name"])
        mock_generate_age.assert_called_once_with(age_min, age_max)
        mock_generate_occupation.assert_called_once_with(ex["age"])
        mock_generate_phone_num.assert_called_once_with() # No arguments expected

        # 2. Verify that the final dictionary returned by generate_person_dict is correct
        assert actual_person_dict == expected_person_dict


    def test_format_person_table_display(self) -> None:
        """
        Tests the format_person_table_display function's output structure and content
        using parametrization for different person data.
        """
        # Setup Mock Person dict
        mock_person_dict = {
            "first_name": "Kory",
            "last_name": "Ahrns",
            "sex": "Male",
            "email": "kory.ahrns@fastmail.com",
            "age": 68,
            "job": "Retired",
            "phone_num": "(705) 385-7324"
        }

        expected_data_str = f"""{BORDER}
          PERSON DETAILS
{BORDER}
{'First Name':<15}: Kory
{'Last Name':<15}: Ahrns
{'Sex':<15}: Male
{'Age':<15}: 68
{'Job':<15}: Retired
{'Phone Num':<15}: (705) 385-7324
{'Email':<15}: kory.ahrns@fastmail.com
{BORDER}"""

        expected_lines_list = expected_data_str.splitlines()

        actual_output = r.format_person_table_display(mock_person_dict)
        actual_lines_list = actual_output.splitlines()

        assert actual_lines_list == expected_lines_list


    def test_format_person_oneline_display(self) -> None:
        """
        Tests the format_person_oneline_display function's output structure and content
        using parametrization for different person data.
        """
        # Setup Mock Person dict
        mock_person_dict = {
            "first_name": "Kory",
            "last_name": "Ahrns",
            "sex": "Male",
            "email": "kory.ahrns@fastmail.com",
            "age": 68,
            "job": "Retired",
            "phone_num": "(705) 385-7324"
        }

        expected_output = (
            "Kory Ahrns            68 Male   Retired                       "
            "(705) 385-7324 kory.ahrns@fastmail.com"
        )
        actual_output = r.format_person_oneline_display(mock_person_dict)
        assert actual_output == expected_output


    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_calls_parse_args(self, mock_parse_args):
        """
        Tests that _parse_args internally calls parser.parse_args().
        This is a very basic sanity check.
        """
        # Call the function
        # pylint: disable=W0212
        r._parse_args()

        # Assert that parse_args was called
        mock_parse_args.assert_called_once()


    def test_parse_args_defaults(self, mocker):
        """
        Tests that _parse_args returns correct default values when no arguments are given.
        """
        # Arrange: Mock sys.argv to simulate no command-line arguments
        # sys.argv[0] is always the script name
        mocker.patch.object(sys, 'argv', ['random_person_generator.py'])

        # Act
        # pylint: disable=W0212
        args = r._parse_args()

        # Assert
        assert args.gender is None
        assert args.min_age == DEFAULT_MIN_AGE
        assert args.max_age == DEFAULT_MAX_AGE
        assert args.count == 1


    def test_parse_args_all_options(self, mocker):
        """
        Tests that _parse_args correctly parses all specified command-line arguments.
        """
        # Arrange: Mock sys.argv to simulate specific command-line arguments
        mocker.patch.object(sys, 'argv', [
            'random_person_generator.py',
            '-g', 'female',
            '--min_age', '25',
            '-max_age', '60',
            '-c', '5'
        ])

        # Act
        # pylint: disable=W0212
        args = r._parse_args()

        # Assert
        assert args.gender == 'female'
        assert args.min_age == 25
        assert args.max_age == 60
        assert args.count == 5


    @pytest.mark.parametrize("gender_input, expected_gender", [
        ("male", "male"),
        ("female", "female"),
    ])
    def test_parse_args_gender_choices(self, mocker, gender_input, expected_gender):
        """
        Tests that _parse_args correctly parses valid gender choices.
        """
        # Arrange: Mock sys.argv to simulate gender inputs
        mocker.patch.object(sys, 'argv', ['random_person_generator.py', '-g', gender_input])

        # Act
        # pylint: disable=W0212
        args = r._parse_args()

        # Assert
        assert args.gender == expected_gender


    def test_parse_args_invalid_gender_raises_error(self, mocker, capsys):
        """
        Tests that _parse_args correctly parses valid gender choices.
        """
        # Arrange: Mock sys.argv to simulate gender inputs
        mocker.patch.object(sys, 'argv', ['random_person_generator.py', '-g', "invalid_gender"])

        # Act
        with pytest.raises(SystemExit) as excinfo:
            # pylint: disable=W0212
            r._parse_args()

        # Assert
        assert excinfo.value.code == 2

        # Check that an error message was printed to stderr
        outerr = capsys.readouterr()
        assert "invalid choice: 'invalid_gender'" in outerr.err


    def test_validate_args_valid_input(self) -> None:
        """
        Tests that _validate_args does not raise an error for valid arguments.
        """
        # Arrange: Create a Namespace object with valid values
        # SimpleNamespace is great for quickly creating objects with attributes
        args = SimpleNamespace(count=1, min_age=18, max_age=60, gender=None)

        # Act & Assert: Call the function. If no exception is raised, the test passes.
        try:
            # pylint: disable=W0212
            r._validate_args(args)
        except SystemExit:
            pytest.fail("_validate_args raised SystemExit for valid input.")


    @pytest.mark.parametrize(
        "count, min_age, max_age, expected_error_message",
        [
            pytest.param(0, 10, 85, "Count must be a positive integer",id="when count==0"),
            pytest.param(-200, 10, 85, "Count must be a positive integer",id="when count==-200"),
            pytest.param(1, -10, 85, "Minimum age cannot be less than zero",id="when min_age==-10"),
            pytest.param(1, 85, 10, "Minimum age cannot be greater than maximum age",
                         id="when min_age==85 and max_age==10"),
        ]
    )
    # pylint: disable=R0917
    def test_validate_args_invalid_age_raises_error(
        self, count, min_age, max_age, expected_error_message, capsys):
        """
        Tests that _validate_args raises SystemExit when count is invalid (<= 0).
        """
        # Arrange
        args = SimpleNamespace(
            count=count, min_age=min_age, max_age=max_age, gender=None)

        # Act & Assert
        with pytest.raises(SystemExit) as excinfo:
            # pylint: disable=W0212
            r._validate_args(args)

        # Assert the exit code and error message
        assert excinfo.value.code == 2 # argparse.error typically exits with code 2
        outerr = capsys.readouterr()
        assert expected_error_message in outerr.err


    def test_validate_args_multiple_errors_prioritization(self, capsys):
        """
        Tests how _validate_args handles multiple invalid conditions.
        It should stop at the first encountered error.
        """
        # Arrange: Both count and age range are invalid
        args = SimpleNamespace(count=0, min_age=50, max_age=40, gender=None)

        # Act & Assert
        with pytest.raises(SystemExit) as excinfo:
            # pylint: disable=W0212
            r._validate_args(args)

        # Assert that only the first error message is present
        assert excinfo.value.code == 2
        outerr = capsys.readouterr()
        assert "Count must be a positive integer." in outerr.err
        assert ("Minimum age cannot be greater than maximum age."
                    not in outerr.err) # Ensure only first error is shown

    @pytest.mark.parametrize(
            "count", [0, 1, 5]
    )
    def test_generate_people_list(self, mocker, count):
        """
        Tests that _test_generate_people_list generates 1 or more person_dict 
        objects
        """
        # Arrange
        args = SimpleNamespace(
            count=count, min_age=10, max_age=85, gender=None)
        expected_person_dict = {"id": "batch_person_data", "name": "Batchy"}

        mock_generate_person_dict = mocker.patch(
            'person_generator.random_person_generator.generate_person_dict',
            return_value=expected_person_dict
        )

        # Act: Call the main function
        # pylint: disable=W0212
        returned_list = r._generate_people_list(args)

        # Assert:
        assert mock_generate_person_dict.call_count == count

        if count > 0:
            mock_generate_person_dict.assert_called_with(
                gender_choice=args.gender, # Default value in main()
                age_min=args.min_age,
                age_max=args.max_age
            )
        else:
            mock_generate_person_dict.assert_not_called()

        assert len(returned_list) == count
        assert returned_list == [expected_person_dict] * count

    @pytest.mark.parametrize(
        "people_data, format_option, expected_person_display_block", 
        TEST_DISPLAY_PEOPLE_CASES
    )
    def test_display_people(
        self, people_data, format_option, expected_person_display_block) -> None:
        """Tests that function r._display_people() returns well formatted display
        of person dictionary data for both oneline and table display formats"""

        args = SimpleNamespace(format=format_option)
        # pylint: disable=W0212
        actual_display_block = r._display_people(people_data, args)

        assert actual_display_block == expected_person_display_block
