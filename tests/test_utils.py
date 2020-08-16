"""Test suite for utils module in the application."""
import pytest
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
