import logging
import pathlib
from typing import Optional

import omegaconf

import expense_viewer.data_loader as loader
import expense_viewer.exceptions as exceptions
import expense_viewer.expense.expense
import expense_viewer.expense.overall_expense as expense

logger = logging.getLogger(__name__)


def get_expense_report(
    config_file_path: str, salary_statement_path: str, statement_bank: str
) -> Optional[expense_viewer.expense.expense.Expense]:
    """
    Get the expense report for the month in the salary statement.

    Parameters
    ----------
    config_file_path : str
        The full path of the config yaml file containing the expense rules.
    salary_statement_path : str
        The full path of the csv file containing the salary statement of the month.
    statement_bank: str
        The bank which the statements come from.
    """
    config_file: pathlib.Path = pathlib.Path(config_file_path)
    salary_statement: pathlib.Path = pathlib.Path(salary_statement_path)
    if not salary_statement.is_dir():
        raise exceptions.StatementPathNotADirectory(
            message="The salary statement path has to be a directory."
        )

    try:
        config = omegaconf.OmegaConf.load(config_file)

        loader.check_format_of_salary_statement(
            salary_statement_paths=salary_statement.glob("*")
        )
        salary_details = loader.load_data_from_all_expense_stmts(
            expense_statements=salary_statement.glob("*"),
            callable=loader.BANK_NAME_TO_CALLABLE[statement_bank],
        )

        expense_obj = expense.OverallExpense(expense=salary_details, config=config)
        expense_obj.add_child_expenses()
        return expense_obj
    except exceptions.Error as exc:
        print(exc)
    except KeyError:
        raise exceptions.BankNotSupportedError(
            "The statements for the banks that are supported are Revolut and Deutsche Bank"
        )

    return None
