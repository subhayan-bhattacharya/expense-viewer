"""File for monthly expenses."""
from typing import Dict, Any, Set
import pandas as pd

import expense_viewer.expense.expense as expense
import expense_viewer.expense.category_expense as category_expense
from expense_viewer import utils as utils


class MonthlyExpense(expense.Expense):
    """Monthly expense category for application."""

    def __init__(
        self, expense: pd.DataFrame, config: Dict[str, Any], label: str = "Overall"
    ) -> None:
        super().__init__(expense=expense, config=config, label=label)
        self._all_found_category_indices: Set[int] = set()
        self._category_indices_map: Dict[str, Set[int]] = dict()

    def add_child_expenses(self):
        """Add the child expenses for the month's items and then delegate."""
        data = self.expense
        for category in self.config:
            condition_str = utils.get_full_condition_string(category)

            expense_data_for_category = data[pd.eval(condition_str)]

            if not expense_data_for_category.empty:
                # Add the child expense only when the data is non empty
                # First check if the indices of the child are already in the found indices for some other category
                # If yes then don't continue further as it is ambiguous
                expense_data_indices = set(expense_data_for_category.index)
                self._expense_data_indices_not_already_found(
                    indices=expense_data_indices
                )
                self._category_indices_map[category] = expense_data_indices

                self.child_expenses[
                    category["name"]
                ] = category_expense.CategoryExpense(
                    expense=expense_data_for_category,
                    config=category,
                    label=category["name"],
                )
                self.child_expenses[category["name"]].add_child_expenses()
            else:
                print(
                    f"No child expenses found for category {category['name']} for the month {self.label}"
                )

    def _expense_data_indices_not_already_found(self, indices: Set[int]) -> None:
        """Check if the indices are already in the set of indices for some other category."""
        for category in self._category_indices_map:
            indices_for_category = self._category_indices_map[category]
            common_indices = indices.intersection(indices_for_category)
            if common_indices:
                raise ValueError(
                    f"There are {common_indices} common indices with category {category}... filter condition needs to be checked."
                )

    def show_expense_summary_graph(self):
        """Show the details of the object's expenses as a bar chart."""
        labels = []
        expenses = []

        for category_name in self.child_expenses:
            child = self.child_expenses[category_name]
            expenses_in_category = round(child.get_total_expense_sum(), 2)

            expenses.append(expenses_in_category)
            labels.append(child.label)

        utils.display_bar_charts(
            labels=labels, axes_labels=["Category", "EUR"], expenses=expenses,
        )

