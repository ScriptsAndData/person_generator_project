"""
Test suite for functions within the display_formatters module using pytest.
"""

from person_generator import random_person_generator as r
from person_generator.display_formatters import BORDER

class TestDisplayFormatters: # No inheritance from unittest.TestCase
    """
    Test suite for functions within the display_formatters module using pytest.
    """

    def test_format_person_table_display(self) -> None:
        """
        Tests the format_person_table_display function's output structure and content
        using parametrization for different person data.
        """
        # Setup Mock Person dict
        mock_person_dict = {
            "first_name": "Kory",
            "last_name": "Ahrns",
            "sex": "Male",
            "email": "kory.ahrns@fastmail.com",
            "age": 68,
            "job": "Retired",
            "phone_num": "(705) 385-7324"
        }

        expected_data_str = f"""{BORDER}
          PERSON DETAILS
{BORDER}
{'First Name':<15}: Kory
{'Last Name':<15}: Ahrns
{'Sex':<15}: Male
{'Age':<15}: 68
{'Job':<15}: Retired
{'Phone Num':<15}: (705) 385-7324
{'Email':<15}: kory.ahrns@fastmail.com
{BORDER}"""

        expected_lines_list = expected_data_str.splitlines()

        actual_output = r.format_person_table_display(mock_person_dict)
        actual_lines_list = actual_output.splitlines()

        assert actual_lines_list == expected_lines_list


    def test_format_person_oneline_display(self) -> None:
        """
        Tests the format_person_oneline_display function's output structure and content
        using parametrization for different person data.
        """
        # Setup Mock Person dict
        mock_person_dict = {
            "first_name": "Kory",
            "last_name": "Ahrns",
            "sex": "Male",
            "email": "kory.ahrns@fastmail.com",
            "age": 68,
            "job": "Retired",
            "phone_num": "(705) 385-7324"
        }

        expected_output = (
            "Kory Ahrns            68 Male   Retired                       "
            "(705) 385-7324 kory.ahrns@fastmail.com"
        )
        actual_output = r.format_person_oneline_display(mock_person_dict)
        assert actual_output == expected_output
