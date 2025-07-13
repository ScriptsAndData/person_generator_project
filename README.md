# Person Generator Project

## Overview

This project provides a simple Python package (`person_generator`) that can generate random person details such as names, email addresses, ages, occupations, and phone numbers. It serves as a practical demonstration of modern Python development best practices, including robust packaging, comprehensive unit testing with multiple frameworks, advanced mocking techniques, and proper resource management within a package.

## Purpose & Showcase

This repository is designed as a portfolio piece to showcase the following technical skills and concepts:

* **Modern Python Packaging:** Utilizes `pyproject.toml` (PEP 621) for project metadata, dependencies, and an editable installation (`pip install -e`). It also correctly configures `package-data` to reliably bundle non-Python assets within the package.
* **Comprehensive Unit Testing:** Includes thorough test suites written in both Python's built-in `unittest` framework and the popular `pytest` framework, demonstrating familiarity with both and precise assertion techniques
* **Advanced Mocking:** Employs `unittest.mock.patch` and `pytest-mock`'s `mocker` fixture to effectively isolate units of code and manage external dependencies, including simulating file I/O, controlling random number generation, and fully isolating complex function chains (e.g., `generate_person_dict`) during testing.
* **Python Package Resource Management:** Demonstrates the correct way to bundle and access data files within a package using `importlib.resources` (or `importlib.files` for Python 3.9+), ensuring reliable access regardless of installation method.
* **Clean Project Structure:** Follows a logical and standard Python package layout.
* **Version Control Best Practices:** (Will be demonstrated via the crafted Git history, showcasing iterative development and problem-solving.)
* **Concise and Pythonic Code:** Demonstrates clean, readable, and efficient Python code, including effective use of f-strings and conditional expressions.

## Features

The `person_generator` package can generate:

* Random male or female first names.
* Random last names.
* Random email addresses based on generated names and common providers.
* Random ages within a typical range.
* Random occupations (distinguishing between "child" and adult jobs).
* Randomly formatted phone numbers.
* A comprehensive dictionary of all generated person details.

## Project Structure
The project adheres to a standard and well-organized Python package structure, promoting clarity and maintainability
```
.
├── LICENSE
├── README.md
├── person_generator
│   ├── init.py
│   ├── data
│   │   ├── init.py
│   │   ├── dist.all.last
│   │   ├── dist.female.first
│   │   └── dist.male.first
│   └── random_person_generator.py
├── pyproject.toml
├── pytests
│   ├── init.py
│   └── test_random_person_generator_pytest.py
├── run_unittests.sh  # Example script (can be removed if pytest is primary runner)
└── unittests
   ├── init.py
   └── test_random_person_generator_unittest.py
```

## Installation

To set up and run this project locally, follow these steps:

1.  **Clone the repository:**
    ```
    git clone https://github.com/your-username/person_generator_project.git

    cd person_generator_project
    ```

2.  **Create and activate a Python virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```
    python -m venv .venv
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows (Cmd):
    .venv\Scripts\activate.bat
    # On Windows (PowerShell):
    .venv\Scripts\Activate.ps1
    ```

3.  **Install the package in editable mode with development dependencies:**

    This will install the `person_generator` package in an 'editable' mode, ensuring changes to the source code are immediately reflected, and will also install `pytest` and `pytest-mock` for testing

    `pip install -e ".[dev]"`

## Usage

You can import and use the `person_generator` module in your Python scripts:

```
# example_usage.py
from person_generator import random_person_generator as rpg

# Generate a random person
person1 = rpg.generate_person_dict()
print("Random Person 1:", person1)

# Generate a female person
person2 = rpg.generate_person_dict(gender='female')
print("Random Person 2 (Female):", person2)

# Access individual generation functions
first_name = rpg.generate_first_name(gender='male')
last_name = rpg.generate_last_name()
email = rpg.generate_email(first_name, last_name)
age = rpg.generate_age()

print(f"\nExample Individual Generation: {first_name} {last_name}, {age}, {email}")
```

To run the example: ```python example_usage.py```

## Running Tests

The project includes unit tests written in both unittest and pytest. pytest is configured to discover and run both sets of tests automatically.

1. Ensure your virtual environment is active (see Installation steps).

2. Run all tests using pytest: 
    
    `pytest`

pytest will discover tests in both pytests/ and unittests/ directories.

To run only the pytest tests:

```pytest pytests/```

To run only the unittest tests (using unittest runner):

```python -m unittest discover unittests -v```

(Note: pytest is generally preferred for running all tests, including unittest ones, due to its enhanced reporting and features.)

## License

This project is licensed under the GNU General Public License v3.0 Only - see the LICENSE file for details.

## Author

[ScriptsAndData](https://github.com/ScriptsAndData)




