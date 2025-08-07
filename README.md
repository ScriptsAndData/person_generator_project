# Person Generator Project

## Overview

This project provides a versatile Python package (`person_generator`) designed to generate realistic random person details, including names, email addresses, ages, occupations, and phone numbers. It stands as a practical demonstration of **robust modern Python development practices**, emphasizing clean architecture, comprehensive testing, and effective resource management.

This repository serves as a **portfolio piece**, meticulously crafted to demonstrate a strong command of contemporary software engineering principles and specific technical skills. It aims to showcase:

## Key Technical Showcases 🚀

The project is built to showcase a deep understanding of several key areas:

* **Comprehensive & Advanced Unit Testing:**
    * **Thorough test suites** utilizing the industry-standard `pytest` framework, demonstrating a deep understanding of testing paradigms.

    * Showcases **data-driven testing patterns** (e.g., using `pytest.mark.parametrize` or custom dictionary-driven loops) for efficient, scalable, and highly readable test cases.

* **Sophisticated Mocking Strategies:**
    * Expert application of `pytest-mock`'s `mocker` fixture to achieve **precise unit isolation**.

    * Demonstrates effective simulation of complex external dependencies, including **mocking file I/O operations** (for data files like names/occupations), **controlling random number generation**, and **fully isolating intricate function chains** to ensure reliable and focused testing.

* **Advanced Python Packaging (`pyproject.toml` & PEP 621):**
    * **Best-in-class project metadata and dependency management** using the modern `pyproject.toml` (PEP 621) standard, ensuring compatibility and streamlined setup.

    * Configured for editable installation (`pip install -e .`) and proper `package-data` bundling, guaranteeing **reliable inclusion and access to non-Python assets** regardless of installation method.

* **Python Package Resource Management:**
    * Implements the **correct and future-proof method** for accessing data files bundled within a package using `importlib.resources` (or `importlib.files` for Python 3.9+). This guarantees reliable data access in any deployment scenario (installed, editable, frozen).

* **Clean & Standard Project Structure:**

  * Strict adherence to a logical and widely accepted Python package layout for clarity and maintainability.

* **Concise and Pythonic Code:**

  * Clean, readable, and efficient Python code, leveraging modern language features like f-strings and conditional expressions.

* **Version Control Best Practices (Git History):**
    * (This will be evident in the repository's Git commit history, which reflects **iterative development, focused commits, and effective problem-solving** throughout the project's evolution.)

## Features

The `person_generator` package is capable of generating:

* Random male or female first names.

* Random last names.

* Random email addresses based on generated names and common providers.

* Random ages within a typical range.

* Random occupations (intelligently distinguishing between "child" and adult jobs based on age).

* Randomly formatted phone numbers.

* A **comprehensive and structured dictionary** containing all generated person details.

## Project Structure

The project adheres to a standard and well-organized Python package structure, promoting clarity and maintainability:

```
├── LICENSE
├── README.md
├── person_generator
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── dist.all.last
│   │   ├── dist.female.first
│   │   ├── dist.male.first
│   │   ├── empty.txt
│   │   ├── list.occupations
│   │   └── numbers_only.txt
│   ├── display_formatters.py
│   └── random_person_generator.py
├── pyproject.toml
└── pytests
    ├── __init__.py
    ├── conftest.py
    ├── test_display_formatters_pytest.py
    └── test_random_person_generator_pytest.py

```

## Installation & Usage

### Prerequisites

You need Python 3.10 or a newer version installed on your system.

### Steps

1.  **Clone the repository:**

    ```
    git clone [https://github.com/your-username/person_generator_project.git](https://github.com/your-username/person_generator_project.git)
    cd person_generator_project
    ```

2.  **Create and activate a virtual environment:**

    ```
    python -m venv .venv
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows (Cmd):
    .venv\Scripts\activate.bat
    ```

3.  **Install the package in editable mode with development dependencies:**
    This will install the `person_generator` package in 'editable' mode and install `pytest` and `pytest-mock` for testing.
    `pip install -e ".[dev]"`

### Example Usage

```
# example_usage.py
from person_generator import random_person_generator as rpg

# Generate a random person
person1 = rpg.generate_person_dict()
print("Random Person 1:", person1)

# Generate a female person with specific age range
person2 = rpg.generate_person_dict(gender='female', min_age=18, max_age=40)
print("Random Person 2 (Female, Adult):", person2)

# Access individual generation functions
first_name = rpg.generate_first_name(gender='male')
last_name = rpg.generate_last_name()
email = rpg.generate_email(first_name, last_name)
age = rpg.generate_age() # Default range
occupation = rpg.generate_occupation(age) # Occupation based on age

print(f"\nExample Individual Generation: {first_name} {last_name}, Age: {age}, Job: {occupation}, Email: {email}")
```


## Unimplemented Improvements (Object-Oriented Refactoring)

During the development and review of this project, a potential refactoring to an object-oriented (OO) design was identified. While the current procedural design is highly effective for the project's primary goal of demonstrating robust unit testing, a more robust OO design would offer improved long-term maintainability and scalability.

This refactoring would involve the creation of dedicated classes:

* **`Person` Class:** This class would encapsulate a person's attributes (e.g., first name, last name, age) and related behavior (e.g., getting a full name). This would eliminate the use of dictionaries, preventing potential `KeyError` bugs and centralizing all data-related logic.

* **`PersonGroup` Class:** This would be a container class to manage a collection of `Person` objects. It would be responsible for operations that act on the group as a whole, such as generating a list of formatted display strings or performing aggregate calculations.

The decision was made to keep the code in its current procedural state to focus on the testing aspect. This improvement is left unimplemented to preserve the current project scope and serves as a documented improvement path for future development.