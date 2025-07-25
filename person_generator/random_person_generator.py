"""
Generate the attributes of a person with random.choice and randint
in a python dictionary
"""
import re
from random import choice, randint
import argparse
from importlib.resources import files as resource_files
from typing import Literal, Optional, List, Dict, Any, Tuple
from pathlib import Path

_DATA_DIR: Path = resource_files('person_generator.data')
GEN_MALE_PATH: Path = _DATA_DIR / "dist.male.first"
GEN_FEMALE_PATH: Path = _DATA_DIR / "dist.female.first"
SURNAME_PATH: Path = _DATA_DIR / "dist.all.last"
JOBS_PATH: Path = _DATA_DIR / "list.occupations"
DEFAULT_MIN_AGE: int = 10
DEFAULT_MAX_AGE: int = 85
RETIREMENT_AGE: int = 67
BECOME_ADULT_AT_AGE: int = 18
EMAIL_PROVIDERS: List[str] = ["aol", "gmail", "outlook", "yahoo", "icloud", "yandex"]


def select_sex(gender_choice: Optional[Literal["male", "female"]] 
                            = None) -> Literal["Male", "Female"]:
    """
    Randomly selects and returns either "Male" or "Female"
    """
    if gender_choice == "male":
        return "Male"
    if gender_choice == "female":
        return "Female"
    return choice(["Male","Female"])

def select_random_name_from_file(file_path: Path) -> str:
    """
    Reads the file containing names, parses it, selects and returns a random name.
    """
    all_names = []
    with open(file_path, 'r', encoding='utf-8') as input_data_io:
        for line in input_data_io:
            thisname = ''.join(re.findall('[a-zA-Z]+', line))
            all_names.append(thisname)
    return choice(all_names).capitalize()

def generate_name(name_type: Literal["first", "last"], 
                  sex: Optional[Literal["Male", "Female"]] = None) -> str:
    """Generates a random first or last name based on the specified type and gender.

    Args:
        name_type (str): The type of name to generate. Must be "first" or "last".
        sex (str, optional): The gender for first names ("Male" or "Female").
                             Required if `name_type` is "first". Defaults to None,
                             which implies a male first name if `name_type` is "first"
                             (due to the `GEN_FEMALE_PATH if sex == "Female" else 
                             GEN_MALE_PATH` logic).

    Returns:
        str: A randomly selected name, capitalized.

    Raises:
        ValueError: If `name_type` is not "first" or "last".
    """
    if name_type == "first":
        file_path = GEN_FEMALE_PATH if sex == "Female" else GEN_MALE_PATH
    elif name_type == "last":
        file_path = SURNAME_PATH
    else:
        raise ValueError("Invalid name_type. Must be 'first' or 'last'.")
    return select_random_name_from_file(file_path)

def generate_email(first_name: str, last_name: str) -> str:
    """
    Returns an email address with a randomly selected surname from the surname file.
    """
    service_provider = choice(EMAIL_PROVIDERS)
    return f"{first_name.lower()}.{last_name.lower()}@{service_provider}.com"

def generate_age(min_age: int = DEFAULT_MIN_AGE, 
                 max_age: int = DEFAULT_MAX_AGE) -> int:
    """Returns randomly generated age"""
    return randint(min_age, max_age)

def generate_phone_num() -> str:
    """Returns randomly generated phone number"""
    return f"0{randint(1000, 9999)} {randint(100, 999)} {randint(0, 999):03d}"

def select_random_job_from_file(file_path: Path) -> str:
    """
    Reads the file containing jobs, parses it, selects and returns a random name.
    """
    all_jobs = []
    with open(file_path, 'r', encoding='utf-8') as input_data_io:
        for line in input_data_io:
            thisjob= ''.join(re.findall('[a-zA-Z ]+', line))
            all_jobs.append(thisjob)
    return choice(all_jobs).title()

def generate_occupation(age: int) -> str:
    """Returns randomly generated job, modified by age"""
    if age > RETIREMENT_AGE:
        job = "Retired"
    elif age >= BECOME_ADULT_AT_AGE:
        job = select_random_job_from_file(JOBS_PATH)
    else:
        job = "Child"
    return job

def generate_person_dict(
        gender_choice: Optional[str], 
        age_min: int, 
        age_max: int) -> Dict[str, Any]:
    """Returns a dictionary object consisting of the all the person attributes"""
    sex = select_sex(gender_choice)
    first_name = generate_name("first", sex)
    last_name = generate_name("last")
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

def format_person_for_display(person_data: Dict[str, Any]) -> str:
    """Formatted standard print for person data"""
    formatted_output  = "-----------------------------------\n"
    formatted_output += "         PERSON DETAILS\n"
    formatted_output += "-----------------------------------\n"
    for key, value in person_data.items():
        formatted_output += f"{key:<15}: {value}\n"
    formatted_output += "-----------------------------------\n"
    return formatted_output


def _get_interactive_person_parameters() -> Tuple[Literal["male", "female", "random"], int, int]:
    """
    Prompts the user for gender and age range and returns the validated inputs.
    """
    print("--- Interactive Person Generation ---")

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
            min_age_str = input(f"Enter minimum age (default {min_age_to_generate}): ").strip()
            min_age_to_generate = int(min_age_str) if min_age_str else min_age_to_generate

            max_age_str = input(f"Enter maximum age (default {max_age_to_generate}): ").strip()
            max_age_to_generate = int(max_age_str) if max_age_str else max_age_to_generate

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


if __name__ == '__main__':
    # Call the main function and capture its return value
    generated_person_data = main()

    print("\nGenerated Person:")
    print(format_person_for_display(generated_person_data))
