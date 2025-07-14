"""
Generate the attributes of a person with random.choice and randint
in a python dictionary
"""
import re
from random import choice, randint
import os
import argparse # Import argparse
from importlib.resources import files as resource_files

_DATA_DIR = resource_files('person_generator.data')
GEN_MALE_PATH = _DATA_DIR / "dist.male.first"
GEN_FEMALE_PATH = _DATA_DIR / "dist.female.first"
SURNAME_PATH = _DATA_DIR / "dist.all.last"
JOBS_PATH = _DATA_DIR / "list.occupations"

def select_sex(gender_choice=None):
    """
    Randomly selects and returns either "Male" or "Female"
    """
    if gender_choice == "male":
        return "Male"
    if gender_choice == "female":
        return "Female"
    return choice(["Male","Female"])

def select_random_name_from_file(file_path):
    """
    Reads the file containing names, parses it, selects and returns a random name.
    """
    all_names = []
    with open(file_path, 'r', encoding='utf-8') as input_data_io:
        for line in input_data_io:
            thisname = ''.join(re.findall('[a-zA-Z]+', line))
            all_names.append(thisname)
    return choice(all_names).capitalize()

def generate_first_name(sex):
    """
    Selects and return a gender matching first name
    """
    file_path = GEN_MALE_PATH if sex == "Male" else GEN_FEMALE_PATH
    return select_random_name_from_file(file_path)

def generate_last_name():
    """
    Returns a randomly selected surname from the surname file.
    """
    return select_random_name_from_file(SURNAME_PATH)

def generate_email(first_name, last_name):
    """
    Returns an email address with a randomly selected surname from the surname file.
    """
    service_provider = choice(["aol", "gmail", "outlook", "yahoo", "icloud", "yandex"])
    return f"{first_name.lower()}.{last_name.lower()}@{service_provider}.com"

def generate_age(min_age=10, max_age=85):
    """Returns randomly generated age"""
    return randint(min_age, max_age)

def generate_phone_num():
    """Returns randomly generated phone number"""
    return f"0{randint(1000, 9999)} {randint(100, 999)} {randint(0, 999):03d}"

def select_random_job_from_file(file_path):
    """
    Reads the file containing jobs, parses it, selects and returns a random name.
    """
    all_jobs = []
    with open(file_path, 'r', encoding='utf-8') as input_data_io:
        for line in input_data_io:
            thisjob= ''.join(re.findall('[a-zA-Z ]+', line))
            all_jobs.append(thisjob)
    return choice(all_jobs).title()

def generate_occupation(age):
    """Returns randomly generated job, modified by age"""
    if age > 67:
        job = "Retired"
    elif age >= 18:
        job = select_random_job_from_file(JOBS_PATH)
    else:
        job = "Child"
    return job

def generate_person_dict(gender_choice=None, age_min=18, age_max=65):
    """Returns a dictionary object consisting of the all the person attributes"""
    sex = select_sex(gender_choice)
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

def format_person_for_display(person_data):
    formatted_output = "-----------------------------------\n"
    formatted_output += "           PERSON DETAILS          \n"
    formatted_output += "-----------------------------------\n"
    for key, value in person_data.items():
        formatted_output += f"{key:<15}: {value}\n"
    formatted_output += "-----------------------------------\n"
    return formatted_output

# Main execution block
if __name__ == '__main__':
    # 1. Set up argument parser
    parser = argparse.ArgumentParser(
        description="Generate random person details. Run in batch mode by default, or interactive mode with --interactive."
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true', # This makes it a boolean flag: True if present, False if not
        help='Run in interactive mode, prompting for gender and age range.'
    )
    # You could also add arguments for directly specifying gender/age in batch mode
    # For example:
    # parser.add_argument('--gender', choices=['male', 'female', 'random'], help='Specify gender (male, female, random) for batch mode.')


    args = parser.parse_args()

    # Initialize variables for person generation parameters
    gender_to_generate = None # Default: let select_sex decide randomly
    min_age_to_generate = 10  # Default
    max_age_to_generate = 85  # Default

    # 2. Check the switch and get input if interactive
    if args.interactive:
        print("--- Interactive Person Generation ---")
        # Get gender input
        while True:
            gender_input = input("Enter desired gender (male/female/random, default: random): ").strip().lower()
            if gender_input in ["male", "female", "random", ""]:
                gender_to_generate = gender_input if gender_input else "random"
                break
            else:
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

    # 3. Generate the person using the determined parameters
    person = generate_person_dict(
        gender_choice=gender_to_generate,
        age_min=min_age_to_generate,
        age_max=max_age_to_generate
    )

    # 4. Display the generated person
    print("\nGenerated Person:")
    print(format_person_for_display(person))
