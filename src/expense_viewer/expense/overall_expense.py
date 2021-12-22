"""Contains the code for displaying the expenses of a single month."""
import collections
import itertools
from typing import Any, Dict, List
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
        self.salary_and_extra_credit_data_per_month: Dict[
            str, Dict[str, int]
        ] = collections.defaultdict(dict)

    def get_expenses_report(self) -> pd.DataFrame:
        """Get a summary of expenses/credits for each month."""
        summary: Dict[str, Any] = collections.defaultdict(list)

        for month in self.child_expenses.keys():
            summary["Month"].append(month)
            summary["Salary"].append(
                self.salary_and_extra_credit_data_per_month[month]["Salary"]
            )
            summary["Extra Credits"].append(
                self.salary_and_extra_credit_data_per_month[month]["Extra Credit"]
            )
            summary["Expenses"].append(
                self.child_expenses[month].get_total_expense_sum()
            )
            summary["Savings"].append(
                self.salary_and_extra_credit_data_per_month[month]["Salary"]
                + self.salary_and_extra_credit_data_per_month[month]["Extra Credit"]
                - self.child_expenses[month].get_total_expense_sum()
            )

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
        for index, data in enumerate(
            itertools.islice(
                utils.break_up_dataframe_in_chunks(self.expense, salary_row_indexes),
                1,
                None,
            )
        ):
            # Check if there are any credits which happened in this month apart from salary
            # if yes then we save them for later summary report
            credit_data_for_month = data[data[_CREDIT_COLUMN_NAME] > 0]
            salary_data_for_month = int(
                self.expense.iloc[[salary_row_indexes[index]]]["Credit"]
            )

            month_year_label = utils.get_expense_month_year(data)

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

            # Save the salary and extra credit data for month
            self.salary_and_extra_credit_data_per_month[month_year_label][
                "Extra Credit"
            ] = sum(credit_data_for_month[_CREDIT_COLUMN_NAME])
            self.salary_and_extra_credit_data_per_month[month_year_label][
                "Salary"
            ] = salary_data_for_month

            self.child_expenses[month_year_label] = monthly_expense.MonthlyExpense(
                expense=data,
                config=expense_categories,
                label=month_year_label,
            )
            # Delegate to the child object to add its own expenses
            self.child_expenses[month_year_label].add_child_expenses()
