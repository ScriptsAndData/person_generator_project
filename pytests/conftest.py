# pytests/conftest.py
"""
Pytest configuration, shared fixtures, and common test data definitions.

This conftest.py file serves as a central place to:
- Define reusable `pytest.param` lists for parameterized tests,
  reducing boilerplate and improving readability in individual test files.
  These lists cover various input scenarios and expected outcomes for core functions
  like `_read_and_process_all_lines_from_file` and specific generators.
- Declare test-specific `Path` constants (e.g., `DATA_EMPTY_PATH`)
  that point to mock or edge-case data files used during testing.
- Import necessary modules and constants that are frequently used across tests,
  promoting consistency.

The definitions within this file are automatically discovered by pytest and
can be imported into test modules to facilitate cleaner and more maintainable
test suites.
"""
from pathlib import Path
import textwrap
from typing import Any # Import Any for more generic dict typing
import pytest

# Import the actual path constants
from person_generator import random_person_generator as r

from person_generator.random_person_generator import (
    _DATA_DIR,
    GEN_MALE_PATH,
    GEN_FEMALE_PATH,
    SURNAME_PATH,
    JOBS_PATH
)
DATA_EMPTY_PATH: Path = _DATA_DIR / "empty.txt"
DATA_NUMBERS_ONLY_PATH: Path = _DATA_DIR / "numbers_only.txt"

# Relates to pytests/test_random_person_generator_pytest.py
    # @pytest.mark.parametrize(
    #     "mock_file_content, file_path_arg, regex_pattern, transform_func, expected_outcome",
    #     TEST_READ_FILE_VARIOUS_INPUTS_CASES
    # )
    # def test_read_files_various_inputs(
TEST_READ_FILE_VARIOUS_INPUTS_CASES:list[Any] = [
    pytest.param(
        textwrap.dedent("""\
            JAMES          3.318  3.318         1
        """),
        GEN_MALE_PATH,
        r'[a-zA-Z]+',
        str.capitalize,
        "James",
        id="male name"
    ),
    pytest.param(
        textwrap.dedent("""\
            MARY           2.629  2.629         1
        """),
        GEN_FEMALE_PATH,
        r'[a-zA-Z]+',
        str.capitalize,
        "Mary",
        id="female name"
    ),
    pytest.param(
        textwrap.dedent("""\
            SMITH          1.006  1.006         1
        """),
        SURNAME_PATH,
        r'[a-zA-Z]+',
        str.capitalize,
        "Smith",
        id="last name"
    ),
    pytest.param(
        textwrap.dedent("""\
            Doctor
        """),
        JOBS_PATH,
        r'[a-zA-Z\s-]+',
        str.title,
        "Doctor",
        id="occupation"
    ),
    pytest.param(
        "", # Empty content
        DATA_EMPTY_PATH,
        r'[a-zA-Z]+',
        str.capitalize,
        ValueError,
        id="empty file"
    ),
    pytest.param(
        "12345\n67890\n", # Content with no match
        DATA_NUMBERS_ONLY_PATH,
        r'[a-zA-Z]+',
        str.capitalize,
        ValueError,
        id="numbers in file / no match"
    )
]

# Relates to pytests/test_random_person_generator_pytest.py
# @pytest.mark.parametrize(
#     ("generator_func, generator_func_args, expected_path, expected_regex,"
#     "expected_transform_func, mock_return_value, read_func_expected_to_be_called"),
#     TEST_GENERATE_RANDOM_VALUE_FROM_FILE
# )
# def test_generate_random_value_from_file(
TEST_GENERATE_RANDOM_VALUE_FROM_FILE: list[Any] = [
    # --- Cases for generate_first_name ---
    pytest.param(
        r.generate_first_name, ('Male',), GEN_MALE_PATH, r'[a-zA-Z]+',
        str.capitalize, "James", True, id="first_name_male_gender"
    ),
    pytest.param(
        r.generate_first_name, ('Female',), GEN_FEMALE_PATH, r'[a-zA-Z]+',
        str.capitalize, "Mary", True, id="first_name_female_gender"
    ),
    # Add a case for unexpected gender if generate_first_name handles it
    # (defaults to female path in your code)
    pytest.param(
        r.generate_first_name, ('Unknown',), GEN_MALE_PATH, r'[a-zA-Z]+',
        str.capitalize, "Alex", True, id="first_name_unknown_gender_defaults_to_male"
    ),

    # --- Cases for generate_last_name ---
    pytest.param(
        r.generate_last_name, (), SURNAME_PATH, r'[a-zA-Z]+',
        str.capitalize, "Catledge", True, id="last_name_generation"
    ),

    # --- Cases for generate_occupation ---
    pytest.param(
        r.generate_occupation, (5,), JOBS_PATH, r'^[a-zA-Z\s]+',
    str.title, "Child", False, id="occupation_child_age_group"
    ),
    pytest.param(
        r.generate_occupation, (40,), JOBS_PATH, r'^[a-zA-Z\s-]+',
        str.title, "Software Engineer", True, id="occupation_adult_age_group"
    ),
    pytest.param(
        r.generate_occupation, (81,), JOBS_PATH, r'^[a-zA-Z\s]+',
        str.title, "Retired", False, id="occupation_senior_age_group"
    ),
    # Add a case for unexpected age_group if generate_occupation handles it
    # (e.g., defaults to general)
    pytest.param(
        r.generate_occupation, (17,), JOBS_PATH, r'^[a-zA-Z\s]+',
        str.title, "Child", False, id="occupation_unknown_age_group_defaults_to_general"
    ),
]
