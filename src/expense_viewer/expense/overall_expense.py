"""Contains the code for displaying the expenses of a single month."""
import pandas as pd
from collections import defaultdict
from typing import Dict, Any
from expense_viewer import expense

import expense_viewer.expense.abs_expense as abs_expense
import expense_viewer.expense.monthly_expense as monthly_expense
import expense_viewer.utils as utils
import expense_viewer


class OverallExpense(abs_expense.Expense):
    """Class for calculating and displaying overall expenses incurred for a list of months."""

    def __init__(
        self, expenses: pd.DataFrame, config: Dict[str, Any], label: str = "Overall"
    ) -> None:
        self.expenses = expenses
        self.config = config
        self.label = label
        self.child_expenses = []
        self.add_child_expenses()  # Creates a child expense for every month

    def add_child_expenses(self):
        """Adds the child expenses for its expense category."""
        expense_categories = self.config["expense_categories"]

        # Read index numbers of salary credited columns
        indexes = utils.get_row_index_for_matching_columns(
            self.config["salary"], self.expenses
        )

        # Divide the expense data into months as per the indexes and assign labels
        # Also add the monthly expense objects into the list of child expenses
        start = 0
        for index in indexes:
            data = self.expenses[start:index]

            month = utils.get_expense_month(data)

            self.child_expenses.append(
                monthly_expense.MonthlyExpense(
                    expense=data, config=expense_categories, label=month
                )
            )

            start = index + 1
        # Add any remaining data after the last salary row in csv
        data = self.expenses[start:]
        if len(data) > 1:
            month = utils.get_expense_month(data)
            self.child_expenses.append(
                monthly_expense.MonthlyExpense(
                    expense=data, config=expense_categories, label=month
                )
            )

    def show_child_expense_labels(self):
        """Just prints the labels of child expenses if any."""
        for child in self.child_expenses:
            print(child.label)

    def show_expense_details(self) -> None:
        """Show expense details for each of the child months."""
        expense_details = defaultdict(list)

        for child in self.child_expenses:
            expenses_in_month = child.show_total_expense_sum()
            savings_in_month = 3373 - expenses_in_month
            print(
                f"Month : {child.label}, Expense: {expenses_in_month} and Savings: {savings_in_month}"
            )
            expense_details["Expenses"].append(expenses_in_month)
            expense_details["Month"].append(child.label)
            expense_details["Savings"].append(savings_in_month)

        pd_dataframe = pd.DataFrame(expense_details)
        pd_dataframe.plot.bar(
            x="Month", y="Expenses", color=expense_viewer.expense_plot_colors
        )

        pd_dataframe.plot.bar(
            x="Month", y="Savings", color=expense_viewer.expense_plot_colors
        )

    def show_total_expense_sum(self) -> None:
        """Show sum total of all the expenses."""
        raise NotImplementedError(
            "This method does not make sense of the Overall expense.."
            "please check child expenses."
        )
