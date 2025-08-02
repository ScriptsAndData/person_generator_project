"""
Test suite for the display_formatters module.

This module contains unit tests for the functions responsible for
formatting person data, ensuring they handle various inputs
(empty lists, single people, multiple people) and output formats
correctly.
"""
import pytest

from person_generator import random_person_generator as r
from .conftest import TEST_FORMAT_PERSON_ONELINE_CASES
from .conftest import TEST_FORMAT_PERSON_TABLE_CASES
from .conftest import TEST_FORMAT_PERSON_DICT_CASES
from .conftest import TEST_FORMAT_PERSON_JSON_CASES


class TestDisplayFormatters: # No inheritance from unittest.TestCase
    """
    A test suite for the formatting functions in `display_formatters.py`.

    This class contains isolated unit tests for `format_person_oneline_display`,
    `format_person_table_display`, `format_person_dict_display`, and
    `format_person_json_display`. It uses pytest's parametrization to test
    a wide range of inputs and expected outputs for each formatter.
    """

    @pytest.mark.parametrize(
        "people_data, expected_person_display_block", 
        TEST_FORMAT_PERSON_ONELINE_CASES
    )
    def test_format_person_oneline_display(
        self, people_data, expected_person_display_block) -> None:
        """
        Test suite for functions within the display_formatters module using pytest.
        """
        # pylint: disable=W0212
        actual_display_block = r.format_person_oneline_display(people_data)

        assert actual_display_block == expected_person_display_block


    @pytest.mark.parametrize(
        "people_data, expected_person_display_block", 
        TEST_FORMAT_PERSON_TABLE_CASES
    )
    def test_format_person_table_display(
        self, people_data, expected_person_display_block) -> None:
        """
        Test suite for functions within the display_formatters module using pytest.
        """
        # pylint: disable=W0212
        actual_display_block = r.format_person_table_display(people_data)

        assert actual_display_block == expected_person_display_block


    @pytest.mark.parametrize(
        "people_data, expected_person_display_block", 
        TEST_FORMAT_PERSON_DICT_CASES
    )
    def test_format_person_dict_display(
        self, people_data, expected_person_display_block) -> None:
        """
        Test suite for functions within the display_formatters module using pytest.
        """
        # pylint: disable=W0212
        actual_display_block = r.format_person_dict_display(people_data)

        assert actual_display_block == expected_person_display_block


    @pytest.mark.parametrize(
        "people_data, expected_person_display_block", 
        TEST_FORMAT_PERSON_JSON_CASES
    )
    def test_format_person_json_display(
        self, people_data, expected_person_display_block) -> None:
        """
        Test suite for functions within the display_formatters module using pytest.
        """
        # pylint: disable=W0212
        actual_display_block = r.format_person_json_display(people_data)

        assert actual_display_block == expected_person_display_block
