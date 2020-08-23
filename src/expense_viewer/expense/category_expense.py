"""File for single category expense."""

from typing import Dict, Any
import pandas as pd

import expense_viewer.expense.abs_expense as abs_expense
from expense_viewer import utils as utils


class CategoryExpense(abs_expense.Expense):
    """A class for a single category of expense."""

    def __init__(
        self, expense: pd.DataFrame, config: Dict[str, Any], label: str
    ) -> None:
        self.expense = expense
        self.label = label
        self.config = config
        self.child_expenses = {}

    def add_child_expenses(self):
        pass

    def show_expense_details(self):
        """Show the expense details for a category."""
        pass

    def show_total_expense_sum(self):
        """Add the total expenses incurred and give it back."""
        pass
