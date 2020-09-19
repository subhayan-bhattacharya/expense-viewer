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

    def show_expense_summary_graph(self):
        """Show the expense details for a category."""
        if not self.child_expenses:
            print("This category expense does not have any child expenses.")
        else:
            super().show_expense_summary_graph()
