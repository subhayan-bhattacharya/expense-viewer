"""Contains the code for displaying the expenses of a single month."""
import collections
import itertools
from typing import Dict, List, Any
import warnings

import omegaconf
import pandas as pd

import expense_viewer.expense.expense as expense
import expense_viewer.expense.monthly_expense as monthly_expense
import expense_viewer.utils as utils

_CREDIT_COLUMN_NAME = "Credit"


class OverallExpense(expense.Expense):
    """Class for calculating and displaying overall expenses incurred for a list of months."""

    def __init__(
        self,
        expense: pd.DataFrame,
        config: omegaconf.dictconfig.DictConfig,
        label: str = "Overall",
    ) -> None:
        super().__init__(expense=expense, config=config, label=label)
        self._extra_credit_data_per_month: Dict[str, int] = {}

    def get_expenses_report(self) -> pd.DataFrame:
        """Get a summary of expenses/credits for each month."""
        summary: Dict[str, Any] = collections.defaultdict(list)

        for month in self.child_expenses.keys():
            summary["Month"].append(month)
            summary["Expenses"].append(
                self.child_expenses[month].get_total_expense_sum()
            )
            summary["Credits"].append(self._extra_credit_data_per_month[month])

        return pd.DataFrame.from_dict(summary)

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
            # Check if there are any credits which happened in this month apart from salary
            # if that is the case then we remove that from expenses
            expense_data_for_month = data[data[_CREDIT_COLUMN_NAME] == 0]

            # But we also want to save the credit
            credit_data_for_month = data[data[_CREDIT_COLUMN_NAME] > 0]

            month_year_label = utils.get_expense_month_year(expense_data_for_month)

            if month_year_label in self.child_expenses.keys():
                # Check if the month is already added then select the next month
                warnings.warn(
                    f"{month_year_label} has already been added to the child expenses..."
                    "adding next month's label to the data"
                )
                month_year_label = utils.get_next_month_label(month_year_label)
                warnings.warn(
                    f"The next month {month_year_label} has been chosen for the data"
                )

            self._extra_credit_data_per_month[month_year_label] = sum(
                credit_data_for_month[_CREDIT_COLUMN_NAME]
            )
            self.child_expenses[month_year_label] = monthly_expense.MonthlyExpense(
                expense=expense_data_for_month,
                config=expense_categories,
                label=month_year_label,
            )
            # Delegate to the child object to add its own expenses
            self.child_expenses[month_year_label].add_child_expenses()

    def get_total_expense_sum(self) -> float:
        """Show sum total of all the expenses."""
        raise NotImplementedError(
            "This method does not make sense of the Overall expense.."
            "please check child expenses."
        )

    def get_expense_summary_dataframe(self) -> pd.DataFrame:
        """Show the expense summary."""
        data: Dict[str, List[int]] = {}

        for label in self.child_expenses:
            child = self.child_expenses[label]
            expenses_in_month = round(child.get_total_expense_sum(), 2)
            savings_in_month = round(3373 - expenses_in_month, 2)
            data[label] = [expenses_in_month, savings_in_month]

        return pd.DataFrame.from_dict(
            data=data, orient="index", columns=["Expenses", "Savings"]
        )
