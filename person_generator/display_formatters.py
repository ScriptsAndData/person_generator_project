"""
This module contains functions for formatting person data for display.

It provides functions to format a dictionary of person attributes into
a single-line string or a multi-line table, suitable for printing to
the console or other output streams. The module is self-contained and
does not depend on the data generation logic.
"""
from typing import Dict, Any

# Define constants specific to display formatting

BORDER: str = "---------------------------------------------"

def format_person_oneline_display(person_data: Dict[str, Any]) -> str:
    """
    Formats person data into a compact single-line string for display,
    using abbreviated job titles.
    """
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
    return formatted_output


def format_person_table_display(person_data: Dict[str, Any]) -> str:
    """
    Formats person data into a multi-line table string for display,
    using abbreviated job titles.
    """
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
    return formatted_output
