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
            'name': 'Category1',
            'logical_operator': 'OR',
            'identifiers': [
                {
                    'value': 'desc1',
                    'comparison_operator': 'contains',
                    'column': 'Payment Details'
                }
            ]
        },
        {
            'name': 'Category2',
            'logical_operator': 'OR',
            'identifiers': [
                {
                    'value': 'desc2',
                    'comparison_operator': 'contains',
                    'column': 'Payment Details'
                }
            ]
        }
    ]
    return config


@pytest.fixture(scope="module")
def expense_data_for_category_1():
    """Return pandas data for category 1"""
    data = {
        "Transaction Type": ["Debit Card Payment"],
        "Payment Details": ["desc1"],
        "Debit": [200.00, 110.10],
        "Credit": [0],
        "Value date": [
            datetime.strptime("05/10/20", "%m/%d/%y"),
        ],
        "Indexes": [0],
    }
    data_pd = pd.DataFrame(data)
    data_pd.set_index("Indexes", inplace=True)
    return data_pd


@pytest.fixture(scope='module')
def expense_data_for_category_2():
    """Return pandas data for category 1"""
    data = {
        "Transaction Type": ["Debit Card Payment", "Debit Card Payment"],
        "Payment Details": ["desc2", "desc2"],
        "Debit": [100.00],
        "Credit": [20.00, 10.00],
        "Value date": [
            datetime.strptime("05/12/20", "%m/%d/%y"),
            datetime.strptime("05/14/20", "%m/%d/%y"),
        ],
        "Indexes": [1, 2],
    }
    data_pd = pd.DataFrame(data)
    data_pd.set_index("Indexes", inplace=True)
    return data_pd


