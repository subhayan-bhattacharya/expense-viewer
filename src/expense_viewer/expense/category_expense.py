"""File for single category expense."""
import pandas as pd

from expense_viewer import utils as utils
import expense_viewer.expense.expense as expense


class CategoryExpense(expense.Expense):
    """A class for a single category of expense."""

    def add_child_expenses(self):
        """Add the child expenses for each subcategory."""
        data = self.expense
        for identifier in self.config["identifiers"]:
            if "label" in identifier:
                # This checks if there is a need to break down the category expense
                # further. No label means that there are no subcategories to the category expense.
                condition_str = utils.get_condition_str_for_single_identifier(
                    identifier=identifier
                )

                expense_data_for_identifier = data[pd.eval(condition_str)]

                if not expense_data_for_identifier.empty:
                    self.child_expenses[identifier["label"]] = expense.Expense(
                        expense=expense_data_for_identifier,
                        config=identifier,
                        label=identifier["label"],
                    )
                # Since the child expense for this is the base class object which does not
                # Have an add_child_expense method, further calls to that method are not done

    def get_total_expense_sum(self) -> float:
        """Sum all the expenses and give back a total sum."""
        return self.expense["Debit"].sum()
