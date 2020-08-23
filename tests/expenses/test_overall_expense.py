"""Test suite for the overall_expense..py module."""
import pandas as pd
from datetime import datetime
import pytest
import expense_viewer.expense.overall_expense as overall_expense


@pytest.fixture(scope="module")
def get_dummy_pandas_data():
    """Produce some dummy pandas data for testing."""
    data = {
        "Transaction Type": [
            "Debit Card Payment",
            "Credit Transfer",
            "Debit Card Payment",
            "Debit Card Payment",
        ],
        "Payment Details": ["Some desc1", "Some desc2", "Some desc3", "Some desc4"],
        "Debit": [100.00, 200.00, 110.10, 150.00],
        "Credit": [330, 2500.89, 337.00, 333.00],
        "Value date": [
            datetime.strptime("05/18/20", "%m/%d/%y"),
            datetime.strptime("11/18/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture(scope="module")
def get_child_expense_dataframe_data():
    """Return a pandas dataframe which is child expense for month of May."""
    data = {
        "Transaction Type": ["Debit Card Payment", "Debit Card Payment"],
        "Payment Details": ["Some desc3", "Some desc4"],
        "Debit": [110.1, 150.0],
        "Credit": [337.0, 333.0],
        "Value date": [
            datetime.strptime("05/14/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
        ],
        "Indexes": [2, 3],
    }
    data_pd = pd.DataFrame(data)
    data_pd.set_index("Indexes", inplace=True)
    return data_pd


@pytest.fixture(scope="module")
def get_dummy_config_data():
    """Produce dummy config data for testing."""
    config = {
        "salary": {
            "logical_operator": "OR",
            "identifiers": [
                {"value": 2500.00, "comparison_operator": ">", "column": "Credit"}
            ],
        },
        "expense_categories": [],
    }
    return config


@pytest.fixture(scope="class")
def init_overall_expense(
    get_dummy_pandas_data,
    get_dummy_config_data,
    get_child_expense_dataframe_data,
    request,
):
    """Initialize the OverallExpense class."""
    obj = overall_expense.OverallExpense(
        expenses=get_dummy_pandas_data, config=get_dummy_config_data
    )
    request.cls.obj = obj
    request.cls.expenses = get_dummy_pandas_data
    request.cls.config = get_dummy_config_data
    request.cls.child_data = get_child_expense_dataframe_data


@pytest.mark.usefixtures("init_overall_expense")
class TestOverallExpense:
    """All the tests for the OverallExpense class."""

    def test_object_of_class_is_created(self):
        """Just assert that the object of class is non empty."""
        assert self.obj is not None
        assert self.obj.config == self.config
        assert self.obj.child_expenses == []
        assert self.obj.label == "Overall"

    def test_add_child_expenses_method(self):
        """Test the functionality of add_child_expenses method of class."""
        self.obj.add_child_expenses()
        assert len(self.obj.child_expenses) == 1
        assert self.obj.child_expenses[0].expense.equals(self.child_data)

    def test_show_child_expense_labels(self):
        """Test the function show_child_expense_labels."""
        assert self.obj.show_child_expense_labels() == ["May"]

    def test_show_total_expense_sum(self):
        """Test the function show_total_expense_sum."""
        with pytest.raises(NotImplementedError):
            self.obj.show_total_expense_sum()

    def test_show_expense_details(self, mocker):
        """Test the function show_expense_details."""
        mocked_display_bar_charts = mocker.patch(
            "expense_viewer.utils.display_bar_charts"
        )
        labels = ["May"]
        expenses = [-409.9]
        savings = [3782.9]
        self.obj.show_expense_details()
        mocked_display_bar_charts.assert_called_with(
            labels=labels,
            axes_labels=["Months", "EUR"],
            expenses=expenses,
            savings=savings,
        )
