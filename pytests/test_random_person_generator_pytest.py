# pytests/test_random_person_generator_pytest.py
"""
Pytest suite for the random_person_generator module.

This module contains tests for functions that generate random person details
such as names, email, age, occupation, and phone numbers.
"""
import re
from typing import Any, Tuple, Callable
from pathlib import Path

import argparse
import sys
from unittest.mock import mock_open, patch
import pytest
from types import SimpleNamespace
from pytest_mock import MockerFixture

from person_generator.random_person_generator import EMAIL_PROVIDERS
from person_generator.random_person_generator import BORDER
from person_generator.random_person_generator import DEFAULT_MAX_AGE
from person_generator.random_person_generator import DEFAULT_MIN_AGE
from person_generator import random_person_generator as r

from .conftest import TEST_READ_FILE_VARIOUS_INPUTS_CASES
from .conftest import TEST_GENERATE_RANDOM_VALUE_FROM_FILE


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

        expected_data_lines = [
            ("first_name", "Kory"),
            ("last_name", "Ahrns"),
            ("sex", "Male"),
            ("email", "kory.ahrns@fastmail.com"),
            ("age", "68"), # Age might be formatted as string in output
            ("job", "Retired"),
            ("phone_num", "(705) 385-7324"),
        ]

        expected_num_lines = 11  # 3 header lines + 7 data lines + 1 end line = 11

        actual_output = r.format_person_table_display(mock_person_dict)
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
            "Kory Ahrns          68 Male   Retired               "
            "(705) 385-7324  kory.ahrns@fastmail.com"
        )
        actual_output = r.format_person_oneline_display(mock_person_dict)
        assert actual_output == expected_output


    @pytest.mark.parametrize(
        "mock_inputs, expected_outputs",
        [
            pytest.param(("male", "11", "81"), ("male", 11, 81), id="inputs args_male_11_81"),
            pytest.param(("female", "25", "61"), ("female", 25, 61), id="inputs args_female_25_61"),
            pytest.param(("", "", ""), ("random", 10, 85), id="inputs args_blank"),
            pytest.param(("random", "", ""), ("random", 10, 85), id="inputs args_random")
        ]
    )
    def test_get_interactive_person_parameters(
        self,
        mocker: MockerFixture,
        mock_inputs: Tuple[str],
        expected_outputs: Tuple[Any]
    ) -> None:
        """Test function _get_interactive_person_parameters() with sets
        of mock interactive inputs"""
        mocker.patch('builtins.input', side_effect=mock_inputs)
        assert r._get_interactive_person_parameters() == expected_outputs


    def test_main_batch_mode_execution(self, mocker: MockerFixture) -> None:
        """
        Tests the main function when run in default (batch) mode.
        Verifies that:
        1. argparse is parsed correctly (no --interactive).
        2. _get_interactive_person_parameters is NOT called.
        3. generate_person_dict is called with default arguments.
        4. main() returns the data from generate_person_dict.
        """
        # Arrange:
        # 1. Mock argparse.ArgumentParser.parse_args to simulate batch mode
        mock_args = mocker.Mock()
        mock_args.interactive = False # Simulate running without -i or --interactive
        mocker.patch('argparse.ArgumentParser.parse_args', return_value=mock_args)

        # 2. Mock _get_interactive_person_parameters to ensure it's NOT invoked
        mock_get_interactive_params = mocker.patch(
            'person_generator.random_person_generator._get_interactive_person_parameters'
        )

        # 3. Mock generate_person_dict to control its return value for main()
        # This is the data main() is expected to return.
        expected_person_data = {"id": "batch_person_data", "name": "Batchy"}
        mock_generate_person_dict = mocker.patch(
            'person_generator.random_person_generator.generate_person_dict',
            return_value=expected_person_data
        )

        # Act: Call the main function
        actual_returned_data = r.main()

        # Assert:
        # 1. Confirm _get_interactive_person_parameters was not called
        mock_get_interactive_params.assert_not_called()

        # 2. Confirm generate_person_dict was called with the expected default arguments
        mock_generate_person_dict.assert_called_once_with(
            gender_choice=None, # Default value in main()
            age_min=r.DEFAULT_MIN_AGE,
            age_max=r.DEFAULT_MAX_AGE
        )

        # 3. Confirm main() returned the expected mocked data
        assert actual_returned_data == expected_person_data


    @pytest.mark.parametrize(
        "interactive_gender_input, interactive_min_age_input, interactive_max_age_input",
        [
            pytest.param("male", 30, 50, id="interactive_male_30_50"),
            pytest.param("female", 15, 25, id="interactive_female_15_25"),
            pytest.param("random", r.DEFAULT_MIN_AGE,
                         r.DEFAULT_MAX_AGE, id="interactive_random_defaults"),
        ]
    )
    def test_main_interactive_mode_execution(
        self,
        mocker: MockerFixture,
        interactive_gender_input: str,
        interactive_min_age_input: int,
        interactive_max_age_input: int
    ) -> None:
        """
        Tests the main function when run in interactive mode.
        Verifies that:
        1. argparse is parsed correctly (--interactive).
        2. _get_interactive_person_parameters is called and its return is used.
        3. generate_person_dict is called with parameters from interactive input.
        4. main() returns the data from generate_person_dict.
        """
        # Arrange:
        # 1. Mock argparse.ArgumentParser.parse_args to simulate interactive mode
        mock_args = mocker.Mock()
        mock_args.interactive = True # Simulate running with -i or --interactive
        mocker.patch('argparse.ArgumentParser.parse_args', return_value=mock_args)

        # 2. Mock _get_interactive_person_parameters to return predefined interactive inputs
        # This avoids re-testing the input parsing logic, which is handled in its own unit test.
        mock_get_interactive_params = mocker.patch(
            'person_generator.random_person_generator._get_interactive_person_parameters',
            return_value=(interactive_gender_input,
                          interactive_min_age_input, interactive_max_age_input)
        )

        # 3. Mock generate_person_dict to control its return value for main()
        expected_person_data = {"id": "interactive_person_data", "name": "Interactively Generated"}
        mock_generate_person_dict = mocker.patch(
            'person_generator.random_person_generator.generate_person_dict',
            return_value=expected_person_data
        )

        # Act: Call the main function
        actual_returned_data = r.main()

        # Assert:
        # 1. Confirm _get_interactive_person_parameters was called
        mock_get_interactive_params.assert_called_once_with()

        # 2. Confirm generate_person_dict was called with the
        # values returned by the interactive mock
        mock_generate_person_dict.assert_called_once_with(
            gender_choice=interactive_gender_input,
            age_min=interactive_min_age_input,
            age_max=interactive_max_age_input
        )

        # 3. Confirm main() returned the expected mocked data
        assert actual_returned_data == expected_person_data


    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_calls_parse_args(self, mock_parse_args):
        """
        Tests that _parse_args internally calls parser.parse_args().
        This is a very basic sanity check.
        """
        # Call the function
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
            r._validate_args(args)
        except SystemExit:
            pytest.fail("_validate_args raised SystemExit for valid input.")


    @pytest.mark.parametrize(
        "count, min_age, max_age, expected_error_message",
        [
            (0, 10, 85, "Count must be a positive integer"),
            (-200, 10, 85, "Count must be a positive integer"),
            (1, -10, 85, "Minimum age cannot be less than zero"),
            (1, 85, 10, "Minimum age cannot be greater than maximum age"),
        ]
    )
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
        returned_list = r._generate_people_list(args)

        # Assert:
        mock_generate_person_dict.call_count == count

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

