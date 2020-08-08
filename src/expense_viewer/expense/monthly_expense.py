"""Contains the code for displaying the expenses of a single month."""
import pandas as pd
from typing import Dict, Any


class MonthlyExpense:
    """Class for calculating and displaying monthly expenses incurred."""

    def __init__(
        self, expenses: pd.core.frame.DataFrame, config: Dict[Any, Any]
    ) -> None:
        self.expenses = expenses
        self.config = config
