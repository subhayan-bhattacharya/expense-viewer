"""File for base class of Expense."""

from typing import Any, Dict, List, Optional

import omegaconf
import pandas as pd


class Expense:
    """Expense base class."""

    def __init__(
        self, expense: pd.DataFrame, config: omegaconf.dictconfig.DictConfig, label: str
    ) -> None:
        self.expense = expense
        self.label = label
        self.config = config
        self.child_expenses: Dict[str, Any] = {}

    def get_child_expense_labels(self) -> Optional[List[str]]:
        """Show the child expense labels associated with the expense object."""
        return list(self.child_expenses.keys()) if self.child_expenses else None

    def get_total_expense_sum(self) -> float:
        """Show sum total of all the expenses."""
        raise NotImplementedError(
            "This method does not make sense of the Overall expense.."
            "please check child expenses."
        )

    def get_expenses_report(self):
        """Get a summary of expenses/credits for each month."""
        raise NotImplementedError(
            "This method is only implemented for overall expense object"
        )
