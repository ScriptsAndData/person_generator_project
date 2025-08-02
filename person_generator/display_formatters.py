"""
This module contains functions for formatting person data for display.

It provides functions to format a list of person dictionaries into
a one-line display, a multi-line table, or a single-block JSON or dict
representation. The module is self-contained and does not depend on the
data generation logic.
"""
import json
from pprint import pformat
from typing import List, Dict, Any

# Define constants specific to display formatting

BORDER: str = "---------------------------------------------"

def format_person_oneline_display(people_list: List[Dict[str, Any]]) -> List[str]:
    """
    Formats a list of person dictionaries into a list of one-line strings.

    Args:
        people_list: A list of dictionaries, where each dictionary
                     represents a single person.

    Returns:
        A list of strings, with each string formatted for a single-line
        console display.
    """
    list_formatted_person_display_strings: List[str] = []
    for person_data in people_list:
        full_name = f'{person_data["first_name"]} {person_data["last_name"]}'

        # Adjusted widths based on your commit diff (20 for name, 29 for job)
        # Re-checked spacing to be clean.
        formatted_output = (
            f'{full_name:<20} '  # Name, left-aligned, 20 chars, then 1 space
            f'{person_data["age"]:>3} '   # Age, right-aligned, 3 chars, then 1 space
            f'{person_data["sex"]:<6} '  # Sex, left-aligned, 6 chars, then 1 space
            f'{person_data["job"]:<29} ' #  Job, left-aligned, 29 chars, then 1 space
            f'{person_data["phone_num"]:<14} ' # Phone, left-aligned, 14 chars, then 1 space
            f'{person_data["email"]}'    # Email
        )
        list_formatted_person_display_strings.append(formatted_output)

    return list_formatted_person_display_strings


def format_person_table_display(people_list: List[Dict[str, Any]]) -> List[str]:
    """
    Formats a list of person dictionaries into a list of multi-line table strings.

    Args:
        people_list: A list of dictionaries, where each dictionary
                     represents a single person.

    Returns:
        A list of strings, with each string representing a complete
        multi-line table block for a single person.
    """
    list_formatted_person_display_strings: List[str] = []
    for person_data in people_list:

        formatted_output = BORDER + "\n"
        formatted_output += "          PERSON DETAILS\n" # Adjusted spacing for center
        formatted_output += BORDER + "\n"
        # Adjusted key widths for better alignment in the table
        formatted_output += f"{'First Name':<15}: {person_data['first_name']}\n"
        formatted_output += f"{'Last Name':<15}: {person_data['last_name']}\n"
        formatted_output += f"{'Sex':<15}: {person_data['sex']}\n"
        formatted_output += f"{'Age':<15}: {person_data['age']}\n"
        formatted_output += f"{'Job':<15}: {person_data['job']}\n"
        formatted_output += f"{'Phone Num':<15}: {person_data['phone_num']}\n"
        formatted_output += f"{'Email':<15}: {person_data['email']}\n"
        formatted_output += BORDER + "\n"

        list_formatted_person_display_strings.append(formatted_output)

    return list_formatted_person_display_strings


def format_person_dict_display(people_list: List[Dict[str, Any]]) -> List[str]:
    """
    Formats a list of person dictionaries into a single string representation
    of a Python list of dictionaries.

    Args:
        people_list: A list of dictionaries, where each dictionary
                     represents a single person.

    Returns:
        A list containing a single string formatted as a pretty-printed
        Python list of dictionaries.
    """
    list_formatted_person_display_strings = [pformat(people_list, indent=2)]
    return list_formatted_person_display_strings


def format_person_json_display(people_list: List[Dict[str, Any]]) -> List[str]:
    """
    Formats a list of person dictionaries into a single string of a
    valid JSON array.

    Args:
        people_list: A list of dictionaries, where each dictionary
                     represents a single person.

    Returns:
        A list containing a single string formatted as a pretty-printed
        JSON array.
    """
    list_formatted_person_display_strings = [json.dumps(people_list, indent=2)]
    return list_formatted_person_display_strings
