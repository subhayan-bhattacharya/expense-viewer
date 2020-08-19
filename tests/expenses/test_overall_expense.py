"""Test suite for the overall_expense..py module."""
import pytest
import expense_viewer.expense.overall_expense as overall_expense


@pytest.fixture(scope="module")
def get_dummy_pandas_data():
    """Produce some dummy pandas data."""


class TestOverallExpense:
    """All the tests for the OverallExpense class."""
