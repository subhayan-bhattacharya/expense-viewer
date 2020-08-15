"""Contains the code for displaying the expenses of a single month."""
import pandas as pd
from typing import Dict, Any

import expense_viewer.expense.abs_expense as abs_expense
import expense_viewer.utils as utils


class OverallExpense(abs_expense.Expense):
    """Class for calculating and displaying overall expenses incurred for a list of months."""

    def __init__(self, expenses: pd.DataFrame, config: Dict[str, Any]) -> None:
        self.expenses = expenses
        self.config = config
        self.label = "Overall"
        self.add_child_expenses()  # Creates a child expense for every month

    def add_child_expenses(self):
        """Adds the child expenses for its expense category."""
        # Read index numbers of salary credited columns
        indexes = utils.get_row_index_for_matching_columns(
            self.config["salary"], self.expenses
        )

        print(indexes)

    def show_child_expense_labels(self):
        pass

    def show_expense_details(self):
        pass
