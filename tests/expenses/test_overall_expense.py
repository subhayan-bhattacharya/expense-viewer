"""Test suite for the overall_expense.py module."""
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
            "Credit Transfer",
            "Debit Card Payment",
        ],
        "Payment Details": ["desc1", "desc2", "desc3", "desc4", "desc5", "desc6"],
        "Debit": [100.00, 200.00, 110.10, 150.00, 140.00, 125.00],
        "Credit": [330, 2500.89, 337.00, 333.00, 2500.89, 320.00],
        "Value date": [
            datetime.strptime("05/18/20", "%m/%d/%y"),
            datetime.strptime("11/18/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
            datetime.strptime("05/16/20", "%m/%d/%y"),
            datetime.strptime("05/18/20", "%m/%d/%y"),
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture(scope="module")
def get_child_expense_dataframe_data_may():
    """Return a pandas dataframe which is child expense for month of May."""
    data = {
        "Transaction Type": ["Debit Card Payment", "Debit Card Payment"],
        "Payment Details": ["desc3", "desc4"],
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
def get_child_expense_dataframe_data_june():
    """Return a pandas dataframe which is child expense for month of May."""
    data = {
        "Transaction Type": ["Debit Card Payment"],
        "Payment Details": ["desc6"],
        "Debit": [125.00],
        "Credit": [320.00],
        "Value date": [datetime.strptime("05/18/20", "%m/%d/%y")],
        "Indexes": [5],
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
    get_child_expense_dataframe_data_may,
    get_child_expense_dataframe_data_june,
    request,
):
    """Initialize the OverallExpense class."""
    obj = overall_expense.OverallExpense(
        expense=get_dummy_pandas_data, config=get_dummy_config_data
    )
    request.cls.obj = obj
    request.cls.expenses = get_dummy_pandas_data
    request.cls.config = get_dummy_config_data
    request.cls.child_data_may = get_child_expense_dataframe_data_may
    request.cls.child_data_june = get_child_expense_dataframe_data_june


@pytest.mark.usefixtures("init_overall_expense")
class TestOverallExpense:
    """All the tests for the OverallExpense class."""

    def test_object_of_class_is_created(self):
        """Just assert that the object of class is non empty."""
        assert self.obj is not None
        assert self.obj.config == self.config
        assert self.obj.child_expenses == {}
        assert self.obj.label == "Overall"

    def test_add_child_expenses_method(self):
        """Test the functionality of add_child_expenses method of class."""
        self.obj.add_child_expenses()
        assert len(list(self.obj.child_expenses.keys())) == 2
        assert self.obj.child_expenses["May"].expense.equals(self.child_data_may)
        assert self.obj.child_expenses["June"].expense.equals(self.child_data_june)

    def test_get_child_expense_labels(self):
        """Test the function get_child_expense_labels."""
        assert self.obj.get_child_expense_labels() == ["May", "June"]

    def test_get_total_expense_sum(self):
        """Test the function get_total_expense_sum."""
        with pytest.raises(NotImplementedError):
            self.obj.get_total_expense_sum()

    def test_show_expense_summary_graph(self, mocker):
        """Test the function show_expense_summary_graph."""
        mocked_display_bar_charts = mocker.patch(
            "expense_viewer.utils.display_bar_charts"
        )
        labels = ["May", "June"]
        expenses = [-409.9, -195.00]
        savings = [3782.9, 3568.00]
        self.obj.show_expense_summary_graph()
        mocked_display_bar_charts.assert_called_with(
            labels=labels,
            axes_labels=["Months", "EUR"],
            expenses=expenses,
            savings=savings,
        )

