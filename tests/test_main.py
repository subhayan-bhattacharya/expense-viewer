import os
import pathlib
import io
import csv


import pandas as pd
import pytest
from ruamel import yaml

import expense_viewer.main as main
import expense_viewer.exceptions as exceptions


def test_read_yaml_file_contents():
    """Test that loading of a yaml file works."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    test_yaml_file = pathlib.Path(current_dir) / "test_data/yaml_test_file.yaml"
    yaml_contents = main.read_yaml_file_contents(test_yaml_file)
    assert yaml_contents == [
        "Casablanca",
        "North by Northwest",
        "The Man Who Wasn't There",
    ]


def test_reading_yaml_error_for_nonexistent_file():
    """Test that loading yaml file gives CouldNotLoadYamlFileError error."""
    yaml_file = pathlib.Path("non_existent_file.yaml")
    with pytest.raises(exceptions.CouldNotLoadYamlFileError):
        main.read_yaml_file_contents(yaml_file)


def test_check_format_of_salary_statement_for_correct_format():
    """Test the function check_format_of_salary_statement works."""
    try:
        main.check_format_of_salary_statement(pathlib.Path("/a/b/c/salary.csv"))
    except Exception:
        pytest.fail("Unexpected error")


def test_check_format_of_salary_statement_for_incorrect_format():
    """Test the function check_format_of_salary_statement fails for wrong format."""
    with pytest.raises(exceptions.WrongFormatError):
        main.check_format_of_salary_statement(pathlib.Path("a/b/c/salary.xls"))


def test_load_details_from_expense_stmt(tmp_path):
    """Test the function load_details_from_expense_stmt."""
    my_dummy_csv_data = [
        [1],
        [2],
        [3],
        [4],
        ["Transaction Type", "Payment Details", "Debit", "Credit"],
        ["T", "Some description", "100", "0"],
        ["F", "Some description2", "150", "20"],
        ["G", "Some description3", "200", 0],
    ]

    dummy_dir = tmp_path / "dummy"
    dummy_dir.mkdir()
    dummy_csv_file = dummy_dir / "dummy_csv.csv"
    with open(dummy_csv_file, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for row in my_dummy_csv_data:
            writer.writerow(row)

    output = main.load_details_from_expense_stmt(dummy_csv_file)

    expected_output = pd.DataFrame(
        {
            "Transaction Type": ["T", "F"],
            "Payment Details": ["Some description", "Some description2"],
            "Debit": ["100", "150"],
            "Credit": ["0", "20"],
        }
    )

    assert list(output.columns.values) == list(expected_output.columns.values)

