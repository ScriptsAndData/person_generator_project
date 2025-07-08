"""
Generate the attributes of a person with random.choice and randint
in a python dictionary
"""
import re
from random import choice, randint

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
