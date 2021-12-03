import csv
import pathlib

import pandas as pd
import pytest

import expense_viewer.exceptions as exceptions
import expense_viewer.main as main


def test_check_format_of_salary_statement_for_correct_format():
    """Test the function check_format_of_salary_statement works."""
    try:
        main.check_format_of_salary_statement([pathlib.Path("/a/b/c/salary.csv")])
    except Exception:
        pytest.fail("Unexpected error")


def test_check_format_of_salary_statement_for_incorrect_format():
    """Test the function check_format_of_salary_statement fails for wrong format."""
    with pytest.raises(exceptions.WrongFormatError):
        main.check_format_of_salary_statement([pathlib.Path("a/b/c/salary.xls")])


def test_load_details_from_expense_stmt(tmp_path):
    """Test the function _load_details_from_expense_stmt."""
    my_dummy_csv_data = [
        [1],
        [2],
        [3],
        [4],
        ["Transaction Type", "Payment Details", "Debit", "Credit", "Value date"],
        ["T", "Some description1", "100.00", "3,300", "05/18/2020"],
        ["T", "Some description2", "150.00", "3,333", "06/23/2020"],
        ["G", "Some description3", "200", "2,500.89", "11/18/2020"],
    ]

    dummy_dir = tmp_path / "dummy"
    dummy_dir.mkdir()
    dummy_csv_file = dummy_dir / "dummy_csv.csv"
    with open(dummy_csv_file, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for row in my_dummy_csv_data:
            writer.writerow(row)

    output = main._load_details_from_expense_stmt(dummy_csv_file)

    expected_output = pd.DataFrame(
        {
            "Transaction Type": ["T", "T"],
            "Payment Details": ["Some description1", "Some description2"],
            "Debit": [100.00, 150.00],
            "Credit": [3300.00, 3333.00],
            "Value date": [pd.to_datetime("05/18/2020"), pd.to_datetime("06/23/2020")],
        }
    )

    assert list(output.columns.values) == list(expected_output.columns.values)
    for column_name in expected_output.columns:
        assert output[column_name].dtype == expected_output[column_name].dtype
        assert list(expected_output[column_name]) == list(output[column_name])
