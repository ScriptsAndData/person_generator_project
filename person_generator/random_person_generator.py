"""
Generate the attributes of a person with random.choice and randint
in a python dictionary
"""
import re
from random import choice, randint
import argparse
from importlib.resources import files as resource_files
from typing import Literal, Optional, List, Dict, Any, Callable
from pathlib import Path

from person_generator.display_formatters import format_person_oneline_display
from person_generator.display_formatters import format_person_table_display
from person_generator.display_formatters import format_person_dict_display
from person_generator.display_formatters import format_person_json_display

_DATA_DIR: Path = resource_files('person_generator.data')
GEN_MALE_PATH: Path = _DATA_DIR / "dist.male.first"
GEN_FEMALE_PATH: Path = _DATA_DIR / "dist.female.first"
SURNAME_PATH: Path = _DATA_DIR / "dist.all.last"
JOBS_PATH: Path = _DATA_DIR / "list.occupations"
DEFAULT_MIN_AGE: int = 10
DEFAULT_MAX_AGE: int = 85
RETIREMENT_AGE: int = 67
BECOME_ADULT_AGE: int = 18
EMAIL_PROVIDERS: List[str] = ["aol", "gmail", "outlook", "yahoo", "icloud",
                              "yandex", "protonmail", "fastmail", "hotmail"]


def generate_sex(gender_choice:
        Optional[Literal["male", "female"]] = None) -> Literal["Male", "Female"]:
    """
    Randomly selects and returns either "Male" or "Female"
    """
    if gender_choice == "male":
        return "Male"
    if gender_choice == "female":
        return "Female"
    return choice(["Male","Female"])


def generate_age(min_age: int = DEFAULT_MIN_AGE,
                 max_age: int = DEFAULT_MAX_AGE) -> int:
    """Returns randomly generated age"""
    return randint(min_age, max_age)


def read_files_various_inputs(
    file_path: Path,
    regex_pattern: str,
    transform_func: Callable[[str], str]
) -> str:
    """
    Reads all lines from a file, extracts strings based on a regex pattern,
    applies a transformation function, and returns a random selection.
    Suitable for small-to-medium sized files where loading into memory is acceptable.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    all_items = []
    with open(file_path, 'r', encoding='utf-8') as input_data_io:
        for line in input_data_io:
            line = line.strip()
            match = re.search(regex_pattern, line)
            if match:
                this_item = match.group(0)
                all_items.append(transform_func(this_item))

    if not all_items:
        raise ValueError(
         f"No items were found from the file : {file_path} with pattern: {regex_pattern}")

    return choice(all_items)


def generate_first_name(gender: str) -> str:
    """Returns randomly generated first name based on gender"""
    path = GEN_FEMALE_PATH if gender == "Female" else GEN_MALE_PATH
    return read_files_various_inputs(
        path, r'[a-zA-Z]+', str.capitalize)


def generate_last_name() -> str:
    """Returns randomly generated last name"""
    return read_files_various_inputs(
        SURNAME_PATH, r'[a-zA-Z]+', str.capitalize)


def generate_occupation(age: int) -> str:
    """Returns randomly generated job, modified by age"""
    if age > RETIREMENT_AGE:
        job = "Retired"
    elif age >= BECOME_ADULT_AGE:
        job = read_files_various_inputs(
            JOBS_PATH, r'^[a-zA-Z\s-]+', str.title)
    else:
        job = "Child"
    return job


def generate_email(first_name: str, last_name: str) -> str:
    """
    Returns an email address with a randomly selected surname from the surname file.
    """
    service_provider = choice(EMAIL_PROVIDERS)
    return f"{first_name.lower()}.{last_name.lower()}@{service_provider}.com"


def generate_phone_num() -> str:
    """
    Returns a randomly generated simple generic-looking phone number.
    Format: (XXX) XXX-XXXX
    """
    # Generates a 3-digit "area code" (no leading 0 here)
    area_code = randint(100, 999)

    # Generates a 3-digit "prefix"
    prefix = randint(100, 999)

    # Generates a 4-digit "line number" (padded with leading zeros if less than 1000)
    line_number = randint(0, 9999)

    return f"({area_code}) {prefix}-{line_number:04d}"


def generate_person_dict(
        gender_choice: Optional[str],
        age_min: int,
        age_max: int) -> Dict[str, Any]:
    """Returns a dictionary object consisting of the all the person attributes"""
    sex = generate_sex(gender_choice)
    first_name = generate_first_name(sex)
    last_name = generate_last_name()
    email = generate_email(first_name, last_name)
    age = generate_age(age_min, age_max)
    job = generate_occupation(age)
    phone_num = generate_phone_num()

    pdict = {
        "first_name": first_name,
        "last_name": last_name,
        "sex": sex,
        "email": email,
        "age": age,
        "job": job,
        "phone_num": phone_num
    }
    return pdict


def _parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate random person data.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-g", "--gender",
        choices=["male", "female"],
        help="Specify gender: 'male' or 'female'. If not specified, a random gender is chosen."
    )
    parser.add_argument(
        "-min_age", "--min_age",
        type=int,
        default=DEFAULT_MIN_AGE,
        help=f"Minimum age for the generated person(s) (default: {DEFAULT_MIN_AGE})."
    )
    parser.add_argument(
        "-max_age", "--max_age",
        type=int,
        default=DEFAULT_MAX_AGE,
        help=f"Maximum age for the generated person(s) (default: {DEFAULT_MAX_AGE})."
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of random people to generate (default: 1)."
    )
    parser.add_argument(
        "-f", "--format",
        choices=["oneline", "table", "dict", "json"],
        default="oneline",
        help="Output format: 'oneline' or 'table' (default: 'oneline')."
    )

    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    """Validates parsed arguments."""
    if args.count <= 0:
        # Use parser.error for graceful exit with help message
        argparse.ArgumentParser().error("Count must be a positive integer.")
    if args.min_age > args.max_age:
        argparse.ArgumentParser().error("Minimum age cannot be greater than maximum age.")
    if args.min_age < 0:
        argparse.ArgumentParser().error("Minimum age cannot be less than zero.")


def _generate_people_list(args: argparse.Namespace) -> List[Dict[str, Any]]:
    """Generates a list of person dictionaries based on validated arguments."""
    generated_people: List[Dict[str, Any]] = []
    for _ in range(args.count):
        person = generate_person_dict(
            gender_choice=args.gender,
            age_min=args.min_age,
            age_max=args.max_age
        )
        generated_people.append(person)
    return generated_people

def get_formatted_display_strings(people_list: List[Dict[str, Any]],
                    args: argparse.Namespace) -> List[str]:
    """
    Formats the list of person dictionaries into a list of strings based on the chosen format.
    Does NOT print directly.
    """
    display_format = args.format

    formatters = {
        "oneline": format_person_oneline_display,
        "table": format_person_table_display,
        "dict": format_person_dict_display,
        "json": format_person_json_display
    }
    # Get the chosen formatter, default to oneline if somehow invalid
    chosen_formatter = formatters.get(display_format, format_person_oneline_display)
    list_formatted_person_display_strings = chosen_formatter(people_list)
    return list_formatted_person_display_strings

def main() -> None: # main now returns None, as it handles printing directly
    """
    Main function to parse arguments, generate, and display random person data.
    """
    args = _parse_args()
    _validate_args(args)
    people_list = _generate_people_list(args)
    list_formatted_person_display_strings = get_formatted_display_strings(people_list, args)

    for person_string in list_formatted_person_display_strings:
        print(person_string)


if __name__ == '__main__':
    main()
