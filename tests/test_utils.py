"""Test suite for utils module in the application."""
import pytest
import pandas as pd
from datetime import datetime
import expense_viewer.utils as utils


@pytest.mark.parametrize(
    "config, expected_output",
    [
        (
            {
                "logical_operator": "OR",
                "identifiers": [
                    {
                        "column": "some_column",
                        "value": 3373.73,
                        "comparison_operator": ">",
                    }
                ],
            },
            'data["some_column"] > 3373.73',
        ),
        (
            {
                "logical_operator": "OR",
                "identifiers": [
                    {
                        "column": "some_column",
                        "value": 3373.73,
                        "comparison_operator": ">",
                    },
                    {
                        "column": "new_column",
                        "comparison_operator": "contains",
                        "value": "some_string",
                    },
                ],
            },
            'data["some_column"] > 3373.73 | data["new_column"].str.contains("some_string")',
        ),
        (
            {
                "logical_operator": "AND",
                "identifiers": [
                    {
                        "column": "some_column",
                        "value": 3373.73,
                        "comparison_operator": ">",
                    },
                    {
                        "column": "new_column",
                        "comparison_operator": "contains",
                        "value": "some_string",
                    },
                ],
            },
            'data["some_column"] > 3373.73 & data["new_column"].str.contains("some_string")',
        ),
    ],
)
def test_get_full_condition_string(config, expected_output):
    """Test the function get_full_condition_string."""
    assert utils.get_full_condition_string(condition=config) == expected_output


@pytest.mark.parametrize(
    "condition_str, expected_value",
    [
        ("data['Credit'] > 2000", [1, 4]),
        ("data['Credit'] > 2000 & data['Details'].str.contains('5')", [4]),
        ("data['Credit'] > 2000 | data['Details'].str.contains('4')", [1, 3, 4]),
    ],
)
def test_get_row_index_for_matching_columns(condition_str, expected_value, mocker):
    """Test the function get_row_index_for_matching_columns."""
    mocked_get_full_condition_string = mocker.patch(
        "expense_viewer.utils.get_full_condition_string"
    )
    mocked_get_full_condition_string.return_value = condition_str
    df = pd.DataFrame(
        {
            "Credit": [0.0, 2800, 0.0, 0.0, 2800, 0.0],
            "Debit": [19.00, 20.00, 25.00, 18.00, 25.00, 20.00],
            "Details": [
                "Detail1",
                "Detail2",
                "Detail3",
                "Detail4",
                "Detail5",
                "Detail6",
            ],
        }
    )
    assert (
        utils.get_row_index_for_matching_columns(condition=dict(), data=df)
        == expected_value
    )


@pytest.mark.parametrize(
    ("data, expected_month"),
    [
        (
            pd.DataFrame(
                {
                    "Value date": [
                        datetime.strptime("05/14/20", "%m/%d/%y"),
                        datetime.strptime("05/12/20", "%m/%d/%y"),
                        datetime.strptime("04/11/20", "%m/%d/%y"),
                        datetime.strptime("03/10/20", "%m/%d/%y"),
                    ]
                }
            ),
            "May",
        ),
        (
            pd.DataFrame(
                {
                    "Value date": [
                        datetime.strptime("06/14/20", "%m/%d/%y"),
                        datetime.strptime("06/12/20", "%m/%d/%y"),
                        datetime.strptime("04/11/20", "%m/%d/%y"),
                        datetime.strptime("03/10/20", "%m/%d/%y"),
                    ]
                }
            ),
            "June",
        ),
    ],
)
def test_get_expense_month(data, expected_month):
    """Test the get_expense_month function inside the utils module."""
    assert utils.get_expense_month(data) == expected_month


@pytest.mark.parametrize(
    ("month, next_month"),
    [("June", "July"), ("January", "February"), ("December", "January")],
)
def test_get_next_month_label(month, next_month):
    """Test for the function get_next_month_label."""
    assert utils.get_next_month_label(month) == next_month
