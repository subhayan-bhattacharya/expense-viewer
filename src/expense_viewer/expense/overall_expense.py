"""Contains the code for displaying the expenses of a single month."""
import collections
import itertools
from typing import Any, Dict
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
        self.salary_savings_credit_data_per_month: Dict[
            str, Dict[str, int]
        ] = collections.defaultdict(dict)
        self.ignored_expenses: Dict[str, pd.DataFrame] = dict()

    def get_expenses_report(self) -> pd.DataFrame:
        """Get a summary of expenses/credits for each month."""
        summary: Dict[str, Any] = collections.defaultdict(list)

        for month in self.child_expenses.keys():
            summary["Month"].append(month)
            summary["Salary"].append(
                self.salary_savings_credit_data_per_month[month]["Salary"]
            )
            summary["Extra Credits"].append(
                self.salary_savings_credit_data_per_month[month]["Extra Credit"]
            )
            summary["Expenses"].append(
                self.child_expenses[month].get_total_expense_sum()
            )
            if "Vaulted Savings" in self.salary_savings_credit_data_per_month[month]:
                summary["Vaulted Savings"].append(
                    self.salary_savings_credit_data_per_month[month]["Vaulted Savings"]
                )
                summary["Savings"].append(
                    self.salary_savings_credit_data_per_month[month]["Salary"]
                    + self.salary_savings_credit_data_per_month[month]["Extra Credit"]
                    - self.child_expenses[month].get_total_expense_sum()
                )
            else:
                summary["Savings"].append(
                    self.salary_savings_credit_data_per_month[month]["Salary"]
                    + self.salary_savings_credit_data_per_month[month]["Extra Credit"]
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
            month_year_label = utils.get_expense_month_year(data)
            # Add the logic for excluding rows which have to be ignored.
            if "ignored" in self.config:
                ignored = self.config["ignored"]
                ignored_data_row_indexes = utils.get_row_index_for_matching_columns(
                    ignored, data
                )
                ignored_expenses = data.index.isin(ignored_data_row_indexes)
                monthly_data_without_ignored_rows = data[~ignored_expenses]
                self.ignored_expenses[month_year_label] = data[ignored_expenses]
            else:
                monthly_data_without_ignored_rows = data

            # Check if there are any credits which happened in this month apart from salary
            # if yes then we save them for later summary report
            credit_data_for_month = monthly_data_without_ignored_rows[
                monthly_data_without_ignored_rows[_CREDIT_COLUMN_NAME] > 0
            ]
            salary_data_for_month = int(
                self.expense.iloc[[salary_row_indexes[index]]]["Credit"]
            )

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

            # Save the salary, extra credit and savings(if any) data for month
            self.salary_savings_credit_data_per_month[month_year_label][
                "Extra Credit"
            ] = sum(credit_data_for_month[_CREDIT_COLUMN_NAME])
            self.salary_savings_credit_data_per_month[month_year_label][
                "Salary"
            ] = salary_data_for_month
            # Let's say the amount of money that you save in a month is transferred to a vault
            # or some other account and you want to consider that transfer as savings
            # and do not want to consider that as an expense
            if "savings" in self.config:
                savings_data_row_indices = utils.get_row_index_for_matching_columns(
                    condition=self.config["savings"],
                    data=monthly_data_without_ignored_rows,
                )
                expense_considered_as_savings = monthly_data_without_ignored_rows[
                    monthly_data_without_ignored_rows.index.isin(
                        savings_data_row_indices
                    )
                ]["Debit"].sum()
                self.salary_savings_credit_data_per_month[month_year_label][
                    "Vaulted Savings"
                ] = expense_considered_as_savings
                self.child_expenses[month_year_label] = monthly_expense.MonthlyExpense(
                    expense=monthly_data_without_ignored_rows,
                    config=expense_categories,
                    label=month_year_label,
                    row_indices_to_ignore=savings_data_row_indices,
                )
            else:
                self.child_expenses[month_year_label] = monthly_expense.MonthlyExpense(
                    expense=monthly_data_without_ignored_rows,
                    config=expense_categories,
                    label=month_year_label,
                )
            # Delegate to the child object to add its own expenses
            self.child_expenses[month_year_label].add_child_expenses()
