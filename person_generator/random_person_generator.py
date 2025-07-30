"""
Generate the attributes of a person with random.choice and randint
in a python dictionary
"""
import re
from random import choice, randint
import argparse
from importlib.resources import files as resource_files
from typing import Literal, Optional, List, Dict, Any, Tuple, Callable
from pathlib import Path

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
BORDER: str = "-----------------------------------"


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


def format_person_table_display(person_data: Dict[str, Any]) -> str:
    """Formatted standard print for person data"""
    formatted_output  = BORDER + "\n"
    formatted_output += "         PERSON DETAILS\n"
    formatted_output += BORDER + "\n"
    for key, value in person_data.items():
        formatted_output += f"{key:<15}: {value}\n"
    formatted_output += BORDER + "\n"
    return formatted_output


def format_person_oneline_display(person_data: Dict[str, Any]) -> str:
    """Formatted standard print for person data"""
    full_name = f'{person_data["first_name"]} {person_data["last_name"]}'
    formatted_output  = (
        f'{full_name:18} '
        f'{person_data["age"]:3} '
        f'{person_data["sex"]:6} '
        f'{person_data["job"]:21} '
        f'{person_data["phone_num"]:14}  '
        f'{person_data["email"]}'
    )
    return formatted_output


def _get_interactive_person_parameters() -> Tuple[Literal["male", "female", "random"], int, int]:
    """
    Prompts the user for gender and age range and returns the validated inputs.
    """
    gender_to_generate = "random" # Default for interactive if user presses enter
    min_age_to_generate = DEFAULT_MIN_AGE # Default for interactive if user presses enter
    max_age_to_generate = DEFAULT_MAX_AGE # Default for interactive if user presses enter

    # Get gender input
    while True:
        gender_input = input("Enter desired gender (male/female/random, default: "
                             f"{gender_to_generate}): ").strip().lower()
        if gender_input in ["male", "female", "random", ""]:
            gender_to_generate = gender_input if gender_input else gender_to_generate
            break
        print("Invalid gender choice. Please enter 'male', 'female', or 'random'.")

    # Get age range input
    while True:
        try:
            min_age_str_input = input(
                f"Enter minimum age (default {min_age_to_generate}): ").strip()
            min_age_to_generate = int(
                min_age_str_input) if min_age_str_input else min_age_to_generate

            max_age_str_input = input(
                f"Enter maximum age (default {max_age_to_generate}): ").strip()
            max_age_to_generate = int(
                max_age_str_input) if max_age_str_input else max_age_to_generate

            if min_age_to_generate > max_age_to_generate:
                print("Minimum age cannot be greater than maximum age. Please re-enter.")
                continue # Loop again for age input
            break # Exit age input loop if valid
        except ValueError:
            print("Invalid age entered. Please enter a number.")

    return gender_to_generate, min_age_to_generate, max_age_to_generate


def main() -> Dict[str, Any]:
    """
    Parses command line options, controls either batch or interactive mode, and 
    returns the generated person data
    """
    parser = argparse.ArgumentParser(
        description="Generate random person details. "
        "Run in batch mode by default, or interactive mode with --interactive."
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode, prompting for gender and age range.'
    )
    args = parser.parse_args()

    gender_final = None # Default for generate_person_dict (random)
    min_age_final = DEFAULT_MIN_AGE
    max_age_final = DEFAULT_MAX_AGE

    if args.interactive:
        gender_final, min_age_final, max_age_final = _get_interactive_person_parameters()

    # Pass parameters to the generation function
    person = generate_person_dict(
        gender_choice=gender_final,
        age_min=min_age_final,
        age_max=max_age_final
    )

    return person


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


# Parses command line options, controls either batch or interactive mode, and
# returns the generated person data.

# Note: This function returns the generated data rather than printing it directly.
# This design choice enhances testability and allows the main function to be
# more easily imported and reused programmatically.
if __name__ == '__main__':

    generated_person_data = main()

    print(format_person_table_display(generated_person_data))
    print(format_person_oneline_display(generated_person_data))


