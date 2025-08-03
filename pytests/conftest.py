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
    get_data_file,
    GEN_MALE_PATH,
    GEN_FEMALE_PATH,
    SURNAME_PATH,
    JOBS_PATH
)
DATA_EMPTY_PATH: Path = get_data_file("empty.txt")
DATA_NUMBERS_ONLY_PATH: Path = get_data_file("numbers_only.txt")

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


# Relates to pytests/test_random_person_generator_pytest.py
# @pytest.mark.parametrize(
#     "people_data, format, expected_person_display_block",
#     TEST_FORMATTED_DISPLAY_STRINGS_CASES
# )
# def test_get_formatted_display_strings(self, mocker,
#         people_data, format, expected_person_display_block) -> None:
TEST_FORMATTED_DISPLAY_STRINGS_CASES: list[Any] = [
    pytest.param(
        [],
        "oneline",
        [],
        id="oneline_empty_input"
    ),
    pytest.param(
        [
            {'first_name': 'Elden', 'last_name': 'Stoehr', 'sex': 'Male',
            'email': 'elden.stoehr@icloud.com', 'age': 11, 'job': 'Child',
            'phone_num': '(325) 276-5577'}],
        "oneline",
        [
            """\
Elden Stoehr          11 Male   Child                         (325) 276-5577 elden.stoehr@icloud.com\
""" # pylint: disable=C0301
        ],
        id="oneline_1person"
    ),
    pytest.param(
        [
            {'first_name': 'Nanette', 'last_name': 'Sisk', 'sex': 'Female',
            'email': 'nanette.sisk@gmail.com', 'age': 81, 'job': 'Retired',
            'phone_num': '(886) 854-6420'},
            {'first_name': 'Zena', 'last_name': 'Mortland', 'sex': 'Female',
            'email': 'zena.mortland@fastmail.com', 'age': 22, 'job':
            'Clinical Rsrch Scientist', 'phone_num': '(617) 226-3654'},
            {'first_name': 'Burton', 'last_name': 'Cothron', 'sex': 'Male',
            'email':'burton.cothron@outlook.com', 'age': 14, 'job': 'Child',
            'phone_num': '(160) 352-2141'}
        ],
        "oneline",
        [
            """\
Nanette Sisk          81 Female Retired                       (886) 854-6420 nanette.sisk@gmail.com\
"""         ,
            """\
Zena Mortland         22 Female Clinical Rsrch Scientist      (617) 226-3654 zena.mortland@fastmail.com\
"""         , # pylint: disable=C0301
            """\
Burton Cothron        14 Male   Child                         (160) 352-2141 burton.cothron@outlook.com\
""" # pylint: disable=C0301
        ],
        id="oneline_3person"
    ),
    pytest.param(
        [
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'}
        ],
            "table",
        [
"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Man
Last Name      : Etherington
Sex            : Male
Age            : 74
Job            : Retired
Phone Num      : (640) 692-8287
Email          : man.etherington@yandex.com
---------------------------------------------
"""
        ],
        id="table_1person"
    ),
        pytest.param(
        [
            {'first_name': 'Ellie', 'last_name': 'Kassam', 'sex': 'Female',
             'email': 'ellie.kassam@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(875) 319-2852'},
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'},
            {'first_name': 'Cyril', 'last_name': 'Gearon', 'sex': 'Male',
             'email': 'cyril.gearon@aol.com', 'age': 23, 'job': 'Location Engineer',
             'phone_num': '(872) 586-5338'}
        ],
            "table",
        [
"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Ellie
Last Name      : Kassam
Sex            : Female
Age            : 74
Job            : Retired
Phone Num      : (875) 319-2852
Email          : ellie.kassam@yandex.com
---------------------------------------------
""",

"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Man
Last Name      : Etherington
Sex            : Male
Age            : 74
Job            : Retired
Phone Num      : (640) 692-8287
Email          : man.etherington@yandex.com
---------------------------------------------
""",

"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Cyril
Last Name      : Gearon
Sex            : Male
Age            : 23
Job            : Location Engineer
Phone Num      : (872) 586-5338
Email          : cyril.gearon@aol.com
---------------------------------------------
"""
        ],
        id="table_3person"
    ),
        pytest.param(
        [
            {'first_name': 'Elden', 'last_name': 'Stoehr', 'sex': 'Male',
            'email': 'elden.stoehr@icloud.com', 'age': 11, 'job': 'Child',
            'phone_num': '(325) 276-5577'}],
        "dict",
        [
            """\
[ { 'age': 11,\n    'email': 'elden.stoehr@icloud.com',\n    'first_name': 'Elden',\n    'job': 'Child',\n    'last_name': 'Stoehr',\n    'phone_num': '(325) 276-5577',\n    'sex': 'Male'}]\
""" # pylint: disable=C0301
        ],
        id="dict_1person"
    ),
            pytest.param(
        [
            {'first_name': 'Ellie', 'last_name': 'Kassam', 'sex': 'Female',
             'email': 'ellie.kassam@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(875) 319-2852'},
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'},
            {'first_name': 'Cyril', 'last_name': 'Gearon', 'sex': 'Male',
             'email': 'cyril.gearon@aol.com', 'age': 23, 'job': 'Location Engineer',
             'phone_num': '(872) 586-5338'}
        ],
            "dict",
        [
"""\
[ { 'age': 74,\n    'email': 'ellie.kassam@yandex.com',\n    'first_name': 'Ellie',\n    'job': 'Retired',\n    'last_name': 'Kassam',\n    'phone_num': '(875) 319-2852',\n    'sex': 'Female'},\n  { 'age': 74,\n    'email': 'man.etherington@yandex.com',\n    'first_name': 'Man',\n    'job': 'Retired',\n    'last_name': 'Etherington',\n    'phone_num': '(640) 692-8287',\n    'sex': 'Male'},\n  { 'age': 23,\n    'email': 'cyril.gearon@aol.com',\n    'first_name': 'Cyril',\n    'job': 'Location Engineer',\n    'last_name': 'Gearon',\n    'phone_num': '(872) 586-5338',\n    'sex': 'Male'}]\
""" # pylint: disable=C0301
        ],
        id="dict_3person"
    ),
        pytest.param(
        [
            {'first_name': 'Elden', 'last_name': 'Stoehr', 'sex': 'Male',
            'email': 'elden.stoehr@icloud.com', 'age': 11, 'job': 'Child',
            'phone_num': '(325) 276-5577'}],
        "json",
        [
            """\
[\n  {\n    "first_name": "Elden",\n    "last_name": "Stoehr",\n    "sex": "Male",\n    "email": "elden.stoehr@icloud.com",\n    "age": 11,\n    "job": "Child",\n    "phone_num": "(325) 276-5577"\n  }\n]\
""" # pylint: disable=C0301
        ],
        id="json_1person"
    ),
            pytest.param(
        [
            {'first_name': 'Ellie', 'last_name': 'Kassam', 'sex': 'Female',
             'email': 'ellie.kassam@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(875) 319-2852'},
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'},
            {'first_name': 'Cyril', 'last_name': 'Gearon', 'sex': 'Male',
             'email': 'cyril.gearon@aol.com', 'age': 23, 'job': 'Location Engineer',
             'phone_num': '(872) 586-5338'}
        ],
            "json",
        [
"""\
[\n  {\n    "first_name": "Ellie",\n    "last_name": "Kassam",\n    "sex": "Female",\n    "email": "ellie.kassam@yandex.com",\n    "age": 74,\n    "job": "Retired",\n    "phone_num": "(875) 319-2852"\n  },\n  {\n    "first_name": "Man",\n    "last_name": "Etherington",\n    "sex": "Male",\n    "email": "man.etherington@yandex.com",\n    "age": 74,\n    "job": "Retired",\n    "phone_num": "(640) 692-8287"\n  },\n  {\n    "first_name": "Cyril",\n    "last_name": "Gearon",\n    "sex": "Male",\n    "email": "cyril.gearon@aol.com",\n    "age": 23,\n    "job": "Location Engineer",\n    "phone_num": "(872) 586-5338"\n  }\n]\
""" # pylint: disable=C0301
        ],
        id="json_3person"
    ),
]


# NEW CODE - UNDER CONSTRUCTION

# Relates to pytests/test_display_formatters_pytest.py
# @pytest.mark.parametrize(
#     "people_data, expected_person_display_block",
#     TEST_FORMAT_PERSON_ONELINE_CASES
# )
# def test_format_person_oneline_display(self, mocker,
#         people_data, expected_person_display_block) -> None:
TEST_FORMAT_PERSON_ONELINE_CASES: list[Any] = [
    pytest.param(
        [],
        [],
        id="empty_input"
    ),
    pytest.param(
        [
            {'first_name': 'Elden', 'last_name': 'Stoehr', 'sex': 'Male',
            'email': 'elden.stoehr@icloud.com', 'age': 11, 'job': 'Child',
            'phone_num': '(325) 276-5577'}],
        [
            """\
Elden Stoehr          11 Male   Child                         (325) 276-5577 elden.stoehr@icloud.com\
""" # pylint: disable=C0301
        ],
        id="1person"
    ),
    pytest.param(
        [
            {'first_name': 'Nanette', 'last_name': 'Sisk', 'sex': 'Female',
            'email': 'nanette.sisk@gmail.com', 'age': 81, 'job': 'Retired',
            'phone_num': '(886) 854-6420'},
            {'first_name': 'Zena', 'last_name': 'Mortland', 'sex': 'Female',
            'email': 'zena.mortland@fastmail.com', 'age': 22, 'job':
            'Clinical Rsrch Scientist', 'phone_num': '(617) 226-3654'},
            {'first_name': 'Burton', 'last_name': 'Cothron', 'sex': 'Male',
            'email':'burton.cothron@outlook.com', 'age': 14, 'job': 'Child',
            'phone_num': '(160) 352-2141'}
        ],
        [
            """\
Nanette Sisk          81 Female Retired                       (886) 854-6420 nanette.sisk@gmail.com\
"""         ,
            """\
Zena Mortland         22 Female Clinical Rsrch Scientist      (617) 226-3654 zena.mortland@fastmail.com\
"""         , # pylint: disable=C0301
            """\
Burton Cothron        14 Male   Child                         (160) 352-2141 burton.cothron@outlook.com\
""" # pylint: disable=C0301
        ],
        id="3person"
    ),
]


# Relates to pytests/test_display_formatters_pytest.py
# @pytest.mark.parametrize(
#     "people_data, expected_person_display_block",
#     TEST_FORMAT_PERSON_TABLE_CASES
# )
# def test_format_person_table_display(self, mocker,
#         people_data, expected_person_display_block) -> None:
TEST_FORMAT_PERSON_TABLE_CASES: list[Any] = [
    pytest.param(
        [],
        [],
        id="empty_input"
    ),
    pytest.param(
        [
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'}
        ],
        [
"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Man
Last Name      : Etherington
Sex            : Male
Age            : 74
Job            : Retired
Phone Num      : (640) 692-8287
Email          : man.etherington@yandex.com
---------------------------------------------
"""
        ],
        id="1person"
    ),
    pytest.param(
        [
            {'first_name': 'Ellie', 'last_name': 'Kassam', 'sex': 'Female',
             'email': 'ellie.kassam@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(875) 319-2852'},
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'},
            {'first_name': 'Cyril', 'last_name': 'Gearon', 'sex': 'Male',
             'email': 'cyril.gearon@aol.com', 'age': 23, 'job': 'Location Engineer',
             'phone_num': '(872) 586-5338'}
        ],
        [
"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Ellie
Last Name      : Kassam
Sex            : Female
Age            : 74
Job            : Retired
Phone Num      : (875) 319-2852
Email          : ellie.kassam@yandex.com
---------------------------------------------
""",
"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Man
Last Name      : Etherington
Sex            : Male
Age            : 74
Job            : Retired
Phone Num      : (640) 692-8287
Email          : man.etherington@yandex.com
---------------------------------------------
""",
"""\
---------------------------------------------
          PERSON DETAILS
---------------------------------------------
First Name     : Cyril
Last Name      : Gearon
Sex            : Male
Age            : 23
Job            : Location Engineer
Phone Num      : (872) 586-5338
Email          : cyril.gearon@aol.com
---------------------------------------------
"""
        ],
        id="3person"
    ),
]


# Relates to pytests/test_display_formatters_pytest.py
# @pytest.mark.parametrize(
#     "people_data, expected_person_display_block",
#     TEST_FORMAT_PERSON_DICT_CASES
# )
# def test_format_person_dict_display(self, mocker,
#         people_data, expected_person_display_block) -> None:
TEST_FORMAT_PERSON_DICT_CASES: list[Any] = [
    pytest.param(
        [],
        ['[]'],
        id="empty_input"
    ),
    pytest.param(
        [
            {'first_name': 'Elden', 'last_name': 'Stoehr', 'sex': 'Male',
            'email': 'elden.stoehr@icloud.com', 'age': 11, 'job': 'Child',
            'phone_num': '(325) 276-5577'}],
        [
            """\
[ { 'age': 11,\n    'email': 'elden.stoehr@icloud.com',\n    'first_name': 'Elden',\n    'job': 'Child',\n    'last_name': 'Stoehr',\n    'phone_num': '(325) 276-5577',\n    'sex': 'Male'}]\
""" # pylint: disable=C0301
        ],
        id="1person"
    ),
    pytest.param(
        [
            {'first_name': 'Ellie', 'last_name': 'Kassam', 'sex': 'Female',
             'email': 'ellie.kassam@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(875) 319-2852'},
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'},
            {'first_name': 'Cyril', 'last_name': 'Gearon', 'sex': 'Male',
             'email': 'cyril.gearon@aol.com', 'age': 23, 'job': 'Location Engineer',
             'phone_num': '(872) 586-5338'}
        ],
        [
"""\
[ { 'age': 74,\n    'email': 'ellie.kassam@yandex.com',\n    'first_name': 'Ellie',\n    'job': 'Retired',\n    'last_name': 'Kassam',\n    'phone_num': '(875) 319-2852',\n    'sex': 'Female'},\n  { 'age': 74,\n    'email': 'man.etherington@yandex.com',\n    'first_name': 'Man',\n    'job': 'Retired',\n    'last_name': 'Etherington',\n    'phone_num': '(640) 692-8287',\n    'sex': 'Male'},\n  { 'age': 23,\n    'email': 'cyril.gearon@aol.com',\n    'first_name': 'Cyril',\n    'job': 'Location Engineer',\n    'last_name': 'Gearon',\n    'phone_num': '(872) 586-5338',\n    'sex': 'Male'}]\
""" # pylint: disable=C0301
        ],
        id="3person"
    ),
]


# Relates to pytests/test_display_formatters_pytest.py
# @pytest.mark.parametrize(
#     "people_data, expected_person_display_block",
#     TEST_FORMAT_PERSON_JSON_CASES
# )
# def test_format_person_json_display(self, mocker,
#         people_data, expected_person_display_block) -> None:
TEST_FORMAT_PERSON_JSON_CASES: list[Any] = [
    pytest.param(
        [],
        ['[]'],
        id="empty_input"
    ),
    pytest.param(
        [
            {'first_name': 'Elden', 'last_name': 'Stoehr', 'sex': 'Male',
            'email': 'elden.stoehr@icloud.com', 'age': 11, 'job': 'Child',
            'phone_num': '(325) 276-5577'}],
        [
            """\
[\n  {\n    "first_name": "Elden",\n    "last_name": "Stoehr",\n    "sex": "Male",\n    "email": "elden.stoehr@icloud.com",\n    "age": 11,\n    "job": "Child",\n    "phone_num": "(325) 276-5577"\n  }\n]\
""" # pylint: disable=C0301
        ],
        id="1person"
    ),
    pytest.param(
        [
            {'first_name': 'Ellie', 'last_name': 'Kassam', 'sex': 'Female',
             'email': 'ellie.kassam@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(875) 319-2852'},
            {'first_name': 'Man', 'last_name': 'Etherington', 'sex': 'Male',
             'email': 'man.etherington@yandex.com', 'age': 74, 'job': 'Retired',
             'phone_num': '(640) 692-8287'},
            {'first_name': 'Cyril', 'last_name': 'Gearon', 'sex': 'Male',
             'email': 'cyril.gearon@aol.com', 'age': 23, 'job': 'Location Engineer',
             'phone_num': '(872) 586-5338'}
        ],
        [
"""\
[\n  {\n    "first_name": "Ellie",\n    "last_name": "Kassam",\n    "sex": "Female",\n    "email": "ellie.kassam@yandex.com",\n    "age": 74,\n    "job": "Retired",\n    "phone_num": "(875) 319-2852"\n  },\n  {\n    "first_name": "Man",\n    "last_name": "Etherington",\n    "sex": "Male",\n    "email": "man.etherington@yandex.com",\n    "age": 74,\n    "job": "Retired",\n    "phone_num": "(640) 692-8287"\n  },\n  {\n    "first_name": "Cyril",\n    "last_name": "Gearon",\n    "sex": "Male",\n    "email": "cyril.gearon@aol.com",\n    "age": 23,\n    "job": "Location Engineer",\n    "phone_num": "(872) 586-5338"\n  }\n]\
""" # pylint: disable=C0301
        ],
        id="3person"
    ),
]
