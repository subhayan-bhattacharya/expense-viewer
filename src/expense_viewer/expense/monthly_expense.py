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

