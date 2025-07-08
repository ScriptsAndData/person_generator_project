"""
Generate the attributes of a person with random.choice and randint
in a python dictionary
"""
from random import choice, randint

def select_sex():
    """
    Randomly selects and returns either "Male" or "Female"
    """
    return choice(["Male","Female"])