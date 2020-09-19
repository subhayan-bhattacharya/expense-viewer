"""File for base class of Expense."""
from typing import List, Optional, Dict, Any
import pandas as pd
from expense_viewer import utils


class Expense:
    """Expense base class."""

    def __init__(
        self, expense: pd.DataFrame, config: Dict[str, Any], label: str
    ) -> None:
        self.expense = expense
        self.label = label
        self.config = config
        self.child_expenses = {}

    def show_expense_summary_graph(self):
        """Method which shows the summary of all the expenses including child ones."""
        """Show the details of the object's expenses as a pie chart."""
        """Other classes can overwrite this and make the chart a bar chart for example."""
        labels = []
        expenses = []

        for category_name in self.child_expenses:
            child = self.child_expenses[category_name]
            expenses_in_category = round(child.get_total_expense_sum(), 2)

            expenses.append(expenses_in_category)
            labels.append(child.label)

        utils.display_pie_charts(
            labels=labels, expenses=expenses,
        )

    def get_child_expense_labels(self) -> Optional[List[str]]:
        """Show the child expense labels associated with the expense object."""
        return list(self.child_expenses.keys()) if self.child_expenses else None

    def get_total_expense_sum(self) -> float:
        """Sum all the expenses and give back a total sum."""
        expense = sum(self.expense["Debit"]) - sum(self.expense["Credit"])
        return expense
