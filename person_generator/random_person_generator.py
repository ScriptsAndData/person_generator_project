"""
Generate the attributes of a person with random.choice and randint
in a python dictionary
"""
import re
from random import choice, randint

from importlib.resources import files as resource_files

_DATA_DIR = resource_files('person_generator.data')
GEN_MALE_PATH = _DATA_DIR / "dist.male.first"
GEN_FEMALE_PATH = _DATA_DIR / "dist.female.first"
SURNAME_PATH = _DATA_DIR / "dist.all.last"

def select_sex():
    """
    Randomly selects and returns either "Male" or "Female"
    """
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

def generate_age():
    """Returns randomly generated age"""
    return randint(1, 100)

def generate_phone_num():
    """Returns randomly generated phone number"""
    return f"0{randint(1000, 9999)} {randint(100, 999)} {randint(0, 999):03d}"

def generate_occupation(age):
    """Returns randomly generated job, modified by age"""
    if age > 67:
        job = "retired"
    elif age >= 18:
        job = choice(["cook", "actor", "programmer", "doctor", "dentist",
                      "uber driver", "photographer", "astronaut", "policeman"])
    elif age >=16:
        job = "student"
    else:
        job = "child"
    return job


