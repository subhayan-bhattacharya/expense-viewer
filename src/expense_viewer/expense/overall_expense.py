"""Contains the code for displaying the expenses of a single month."""
import warnings
import itertools

import omegaconf
import pandas as pd

import expense_viewer.expense.expense as expense
import expense_viewer.expense.monthly_expense as monthly_expense
import expense_viewer.utils as utils


class OverallExpense(expense.Expense):
    """Class for calculating and displaying overall expenses incurred for a list of months."""

    def __init__(
        self,
        expense: pd.DataFrame,
        config: omegaconf.dictconfig.DictConfig,
        label: str = "Overall",
    ) -> None:
        super().__init__(expense=expense, config=config, label=label)

    def add_child_expenses(self):
        """Adds the child expenses for its expense category."""
        expense_categories = self.config["expense_categories"]

        # Read index numbers of salary credited columns
        salary_row_indexes = utils.get_row_index_for_matching_columns(
            self.config["salary"], self.expense
        )

        # Divide the expense data into months as per the indexes and assign labels
        # The data before the first salary row is not taken into account
        # Also add the monthly expense objects into the list of child expenses
        for data in itertools.islice(
            utils.break_up_dataframe_in_chunks(self.expense, salary_row_indexes),
            1,
            None,
        ):
            month = utils.get_expense_month(data)

            if month in self.child_expenses.keys():
                # Check if the month is already added then select the next month
                warnings.warn(
                    f"{month} has already been added to the child expenses..."
                    "adding next month's label to the data"
                )
                month = utils.get_next_month_label(month)
                warnings.warn(f"The next month {month} has been chosen for the data")

            self.child_expenses[month] = monthly_expense.MonthlyExpense(
                expense=data, config=expense_categories, label=month
            )
            # Delegate to the child object to add its own expenses
            self.child_expenses[month].add_child_expenses()

    def show_expense_summary_graph(self) -> None:
        """Show expense details for each of the child months."""
        labels = []
        expenses = []
        savings = []

        for label in self.child_expenses:
            child = self.child_expenses[label]
            expenses_in_month = round(child.get_total_expense_sum(), 2)
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

    def get_total_expense_sum(self) -> float:
        """Show sum total of all the expenses."""
        raise NotImplementedError(
            "This method does not make sense of the Overall expense.."
            "please check child expenses."
        )
