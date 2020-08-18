"""File for abstract class of Expense."""
import abc
from typing import List


class Expense(abc.ABC):
    """Expense abstract class."""

    @abc.abstractmethod
    def show_expense_details(self):
        """Abstract method to show details of expenses."""
        ...

    @abc.abstractmethod
    def show_child_expense_labels(self) -> List[str]:
        """Show the child expense labels associated with the expense object."""
        ...

    @abc.abstractmethod
    def show_total_expense_sum(self) -> float:
        """Sum all the expenses and give back a total sum."""
