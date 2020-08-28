"""File for base class of Expense."""
from typing import List, Optional, Dict, Any
import pandas as pd


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
        raise NotImplementedError(
            "This method is not implemented in this category of object"
        )

    def get_child_expense_labels(self) -> Optional[List[str]]:
        """Show the child expense labels associated with the expense object."""
        return list(self.child_expenses.keys()) if self.child_expenses else None

    def get_total_expense_sum(self) -> float:
        """Sum all the expenses and give back a total sum."""
        expense = sum(self.expense["Debit"]) - sum(self.expense["Credit"])
        return expense
