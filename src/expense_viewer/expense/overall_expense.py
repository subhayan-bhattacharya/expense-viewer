"""Contains the code for displaying the expenses of a single month."""
import pandas as pd
from typing import Dict, Any

import expense_viewer.expense.abs_expense as abs_expense


class OverallExpense(abs_expense.Expense):
    """Class for calculating and displaying overall expenses incurred for a list of months."""

    def __init__(
        self, monthly_expenses: pd.core.frame.DataFrame, config: Dict[Any, Any]
    ) -> None:
        self.expenses = monthly_expenses
        self.config = config
