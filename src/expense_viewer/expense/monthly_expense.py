"""File for monthly expenses."""
from typing import Dict, Any
import pandas as pd

import expense_viewer.expense.abs_expense as abs_expense
import expense_viewer.expense.category_expense as category_expense
from expense_viewer import utils as utils
from expense_viewer.expense.category_expense import CategoryExpense


class MonthlyExpense(abs_expense.Expense):
    """Monthly expense category for application."""

    def __init__(
        self, expense: pd.DataFrame, config: Dict[str, Any], label: str
    ) -> None:
        self.expense = expense
        self.label = label
        self.config = config
        self.child_expenses = {}

    def add_child_expenses(self):
        """Add the child expenses for the month's items and then delegate."""
        data = self.expense
        for category in self.config:
            condition_str = utils.get_full_condition_string(category)

            expense_data_for_category = data[pd.eval(condition_str)]

            if not expense_data_for_category.empty:
                # Add the child expense only when the data is non empty
                self.child_expenses[
                    category["name"]
                ] = category_expense.CategoryExpense(
                    expense=expense_data_for_category,
                    config=category,
                    label=category["name"],
                )
                # self.child_expenses[category["name"]].add_child_expenses()

    def show_expense_details(self):
        pass

    def show_total_expense_sum(self) -> float:
        """Find the sum total of all expenses in the month."""
        expense = sum(self.expense["Debit"]) - sum(self.expense["Credit"])
        return expense
