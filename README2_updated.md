# Person Generator Project

## Overview

This project provides a versatile Python package (`person_generator`) designed to generate realistic random person details, including names, email addresses, ages, occupations, and phone numbers. It stands as a practical demonstration of **robust modern Python development practices**, emphasizing clean architecture, comprehensive testing, and effective resource management.

## Purpose & Technical Showcase 🚀

This repository serves as a **portfolio piece**, meticulously crafted to demonstrate a strong command of contemporary software engineering principles and specific technical skills. It aims to showcase:

* **Advanced Python Packaging (`pyproject.toml` & PEP 621):**
    * **Best-in-class project metadata and dependency management** using the modern `pyproject.toml` (PEP 621) standard, ensuring compatibility and streamlined setup.
    * Configured for editable installation (`pip install -e .`) and proper `package-data` bundling, guaranteeing **reliable inclusion and access to non-Python assets** regardless of installation method.
* **Comprehensive & Advanced Unit Testing:**
    * **Thorough test suites** utilizing both Python's built-in `unittest` framework and the industry-standard `pytest` framework, demonstrating versatility and a deep understanding of testing paradigms.
    * Showcases **data-driven testing patterns** (e.g., using `pytest.mark.parametrize` or custom dictionary-driven loops) for efficient, scalable, and highly readable test cases, especially visible in the `test_random_person_generator_pytest.py` file.
* **Sophisticated Mocking Strategies:**
    * Expert application of `unittest.mock.patch` and `pytest-mock`'s `mocker` fixture to achieve **precise unit isolation**.
    * Demonstrates effective simulation of complex external dependencies, including **mocking file I/O operations** (for data files like names/occupations), **controlling random number generation**, and **fully isolating intricate function chains** (e.g., the `generate_person_dict` orchestration logic) to ensure reliable and focused testing.
* **Python Package Resource Management:**
    * Implements the **correct and future-proof method** for accessing data files bundled within a package using `importlib.resources` (or `importlib.files` for Python 3.9+). This guarantees reliable data access in any deployment scenario (installed, editable, frozen).
* **Clean & Standard Project Structure:**
    * Adheres strictly to a **logical and widely accepted Python package layout**, promoting clarity, maintainability, and ease of navigation for other developers.
* **Version Control Best Practices (Git History):**
    * (This will be evident in the repository's Git commit history, which reflects **iterative development, focused commits, and effective problem-solving** throughout the project's evolution.)
* **Concise and Pythonic Code:**
    * Demonstrates **clean, readable, and efficient Python code**, leveraging modern language features such as f-strings and conditional expressions for improved clarity and performance.

## Features

The `person_generator` package is capable of generating:

* Random male or female first names.
* Random last names.
* Random email addresses based on generated names and common providers.
* Random ages within a typical range.
* Random occupations (intelligently distinguishing between "child" and adult jobs based on age).
* Randomly formatted phone numbers.
* A **comprehensive and structured dictionary** containing all generated person details.

## Development Status

This project is under active **Test-Driven Development (TDD)**.

* **Pytest Suite:** The `pytests` suite is fully updated and passing, reflecting the latest feature implementations and demonstrating the project's core functionality.
* **Unittest Suite:** The `unittests` suite is currently in a transitional state and is expected to have failures. It will be updated and brought to full parity with the `pytests` in a subsequent development cycle.

To run only the `pytests`, use the command: `pytest pytests/` or `./run_tests.sh` (if `run_tests.sh` executes only `pytests`).

## Project Structure

The project adheres to a standard and well-organized Python package structure, promoting clarity and maintainability:
```

├── LICENSE
├── README.md
├── person_generator
│   ├── init.py
│   ├── data
│   │   ├── init.py
│   │   ├── dist.all.last
│   │   ├── dist.female.first
│   │   ├── dist.male.first
│   │   └── list.occupations
│   └── random_person_generator.py
├── pyproject.toml
├── pytests
│   ├── init.py
│   └── test_random_person_generator_pytest.py
├── run_unittests.sh
└── unittests
   ├── init.py
   └── test_random_person_generator_unittest.py
```
## Installation

To set up and run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/person_generator_project.git](https://github.com/your-username/person_generator_project.git)
    cd person_generator_project
    ```

2.  **Create and activate a Python virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv .venv
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows (Cmd):
    .venv\Scripts\activate.bat
    # On Windows (PowerShell):
    .venv\Scripts\Activate.ps1
    ```

3.  **Install the package in editable mode with development dependencies:**

    This will install the `person_generator` package in an 'editable' mode, ensuring changes to the source code are immediately reflected, and will also install `pytest` and `pytest-mock` for testing.

    `pip install -e ".[dev]"`

## Usage

You can import and use the `person_generator` module in your Python scripts:

```python
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
