"""Contains the code for displaying the expenses of a single month."""
import pandas as pd
from typing import Dict, Any, List

import expense_viewer.expense.abs_expense as abs_expense
import expense_viewer.expense.monthly_expense as monthly_expense
import expense_viewer.utils as utils


class OverallExpense(abs_expense.Expense):
    """Class for calculating and displaying overall expenses incurred for a list of months."""

    def __init__(
        self, expenses: pd.DataFrame, config: Dict[str, Any], label: str = "Overall"
    ) -> None:
        self.expenses = expenses
        self.config = config
        self.label = label
        self.child_expenses = {}

    def add_child_expenses(self):
        """Adds the child expenses for its expense category."""
        expense_categories = self.config["expense_categories"]

        # Read index numbers of salary credited columns
        salary_row_indexes = utils.get_row_index_for_matching_columns(
            self.config["salary"], self.expenses
        )

        # Divide the expense data into months as per the indexes and assign labels
        # The data before the first salary row is not taken into account
        # Also add the monthly expense objects into the list of child expenses
        for index, value in enumerate(salary_row_indexes):
            data = (
                self.expenses[value + 1 :]
                if len(salary_row_indexes) - 1 == index
                else self.expenses[value + 1 : salary_row_indexes[index + 1]]
            )

            month = utils.get_expense_month(data)

            self.child_expenses[month] = monthly_expense.MonthlyExpense(
                expense=data, config=expense_categories, label=month
            )

    def show_expense_details(self) -> None:
        """Show expense details for each of the child months."""
        labels = []
        expenses = []
        savings = []

        for label in self.child_expenses:
            child = self.child_expenses[label]
            expenses_in_month = round(child.show_total_expense_sum(), 2)
            savings_in_month = round(3373 - expenses_in_month, 2)

            expenses.append(expenses_in_month)
            savings.append(savings_in_month)
            labels.append(child.label)

        utils.display_bar_charts(
            labels=labels,
            axes_labels=["Months", "EUR"],
            expenses=expenses,
            savings=savings,
        )

    def show_total_expense_sum(self) -> None:
        """Show sum total of all the expenses."""
        raise NotImplementedError(
            "This method does not make sense of the Overall expense.."
            "please check child expenses."
        )
