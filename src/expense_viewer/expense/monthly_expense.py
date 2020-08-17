"""File for monthly expenses."""
from typing import Dict, Any
import pandas as pd

import expense_viewer.expense.abs_expense as abs_expense


class MonthlyExpense(abs_expense.Expense):
    """Monthly expense category for application."""

    def __init__(
        self, expense: pd.DataFrame, config: Dict[str, Any], label: str
    ) -> None:
        self.expense = expense
        self.label = label
        self.config = config
        self.child_expenses = []

    def show_child_expense_labels(self):
        pass

    def show_expense_details(self):
        pass
