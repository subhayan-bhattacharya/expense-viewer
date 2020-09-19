"""Test suite for the monthly_expense.py file."""
import pandas as pd
from datetime import datetime
import pytest
import expense_viewer.expense.monthly_expense as monthly_expense


@pytest.fixture(scope="module")
def get_dummy_pandas_data():
    """Create some dummy pandas data."""
    data = {
        "Transaction Type": [
            "Debit Card Payment",
            "Debit Card Payment",
            "Debit Card Payment",
        ],
        "Payment Details": ["desc1", "desc2", "desc2"],
        "Debit": [100.00, 200.00, 110.10],
        "Credit": [0, 20.00, 10.00],
        "Value date": [
            datetime.strptime("05/10/20", "%m/%d/%y"),
            datetime.strptime("05/12/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture(scope="module")
def get_dummy_config_data():
    """Produce dummy config data for testing."""
    config = [
        {
            "name": "Category1",
            "logical_operator": "OR",
            "identifiers": [
                {
                    "value": "desc1",
                    "comparison_operator": "contains",
                    "column": "Payment Details",
                    "label": "Category1",
                }
            ],
        },
        {
            "name": "Category2",
            "logical_operator": "OR",
            "identifiers": [
                {
                    "value": "desc2",
                    "comparison_operator": "contains",
                    "column": "Payment Details",
                    "label": "Category2",
                }
            ],
        },
    ]
    return config


@pytest.fixture(scope="module")
def expense_data_for_category_1():
    """Return pandas data for category 1"""
    data = {
        "Transaction Type": ["Debit Card Payment"],
        "Payment Details": ["desc1"],
        "Debit": [100.00],
        "Credit": [0.0],
        "Value date": [datetime.strptime("05/10/20", "%m/%d/%y")],
    }
    data_pd = pd.DataFrame(data)
    data_pd.set_index([[0]], inplace=True)
    return data_pd


@pytest.fixture(scope="module")
def expense_data_for_category_2():
    """Return pandas data for category 1"""
    data = {
        "Transaction Type": ["Debit Card Payment", "Debit Card Payment"],
        "Payment Details": ["desc2", "desc2"],
        "Debit": [200.00, 110.10],
        "Credit": [20.00, 10.00],
        "Value date": [
            datetime.strptime("05/12/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
        ],
    }
    data_pd = pd.DataFrame(data)
    data_pd.set_index([[1, 2]], inplace=True)
    return data_pd


@pytest.fixture(scope="class")
def init_monthly_expense(
    get_dummy_pandas_data,
    get_dummy_config_data,
    expense_data_for_category_1,
    expense_data_for_category_2,
    request,
):
    """Initialize the OverallExpense class."""
    obj = monthly_expense.MonthlyExpense(
        expense=get_dummy_pandas_data, config=get_dummy_config_data, label="May"
    )
    request.cls.obj = obj
    request.cls.expenses = get_dummy_pandas_data
    request.cls.config = get_dummy_config_data
    request.cls.child_data_category_1 = expense_data_for_category_1
    request.cls.child_data_category_2 = expense_data_for_category_2


@pytest.mark.usefixtures("init_monthly_expense")
class TestMonthlyExpense:
    """All the tests for the MonthlyExpense class."""

    def test_object_of_class_is_created(self):
        """Just assert that the object of class is non empty."""
        assert self.obj is not None
        assert self.obj.config == self.config
        assert self.obj.child_expenses == {}
        assert self.obj.label == "May"

    def test_add_child_expenses_method(self):
        """Test the functionality of add_child_expenses method of class."""
        self.obj.add_child_expenses()
        assert len(list(self.obj.child_expenses.keys())) == 2
        assert self.obj.child_expenses["Category1"].expense.equals(
            self.child_data_category_1
        )
        assert self.obj.child_expenses["Category2"].expense.equals(
            self.child_data_category_2
        )

    def test_show_expense_summary_graph(self, mocker):
        """Test the method show_expense_summary_graph of the monthly expense class."""
        mocked_display_pie_charts = mocker.patch(
            "expense_viewer.utils.display_pie_charts"
        )
        self.obj.show_expense_summary_graph()
        mocked_display_pie_charts.assert_called_with(
            labels=["Category1", "Category2"], expenses=[100.00, 280.10]
        )
