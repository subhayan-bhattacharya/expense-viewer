import logging
import pathlib
import typing

import omegaconf
import pandas as pd

import expense_viewer.exceptions as exceptions
import expense_viewer.expense.expense
import expense_viewer.expense.overall_expense as expense

EXPECTED_FORMATS = (".csv",)

logger = logging.getLogger(__name__)


def replace_comma_if_string(value: typing.Union[str, float]):
    """Check if the value is a string then do replacement of comma."""
    if isinstance(value, str):
        return value.replace(",", "")
    return value


def check_format_of_salary_statement(
    salary_statement_paths: typing.Iterable[pathlib.Path],
) -> None:
    """
    Check that the format of salary statement is in the right format.

    Parameters
    ----------
    salary_statement_paths : Iterable[pathlib.Path]
        An iterable of salary statement paths.

    Raises
    ------
    WrongFormatError
        When the format of the salary statement is not right
    """
    for salary_statement_path in salary_statement_paths:
        format_of_file = salary_statement_path.suffix
        if format_of_file not in EXPECTED_FORMATS:
            message = f"The file {salary_statement_path} is not in right format"
            logger.error(message)
            raise exceptions.WrongFormatError(message=message)


def load_details_from_expense_stmt(
    expense_statement: pathlib.Path,
) -> pd.core.frame.DataFrame:
    """
    Load the expense details from csv file and get back a pandas dataframe.

    Parameters
    ----------
    expense_statement : pathlib.Path
        The expense statement full path as a csv file
    """
    columns_to_use = [
        "Transaction Type",
        "Payment Details",
        "Debit",
        "Credit",
        "Value date"
    ]

    try:
        transactions = pd.read_csv(
            expense_statement,
            encoding="latin",
            error_bad_lines=False,
            skiprows=4,
            delimiter=";",
            usecols=columns_to_use,
        )
        transactions.drop(transactions.tail(1).index, inplace=True)
        transactions["Credit"] = transactions["Credit"].apply(replace_comma_if_string)
        transactions["Debit"] = transactions["Debit"].apply(replace_comma_if_string)
        transactions["Credit"] = transactions["Credit"].astype("float64")
        transactions["Debit"] = transactions["Debit"].astype("float64")
        transactions["Value date"] = transactions["Value date"].astype("datetime64")
        transactions["Credit"].fillna(0, inplace=True)
        transactions["Debit"].fillna(0, inplace=True)
        transactions["Debit"] = transactions["Debit"].apply(
            lambda value: value if value >= 0 else value * -1
        )
        return transactions
    except Exception as exc:
        message = f"Could not load the details from {expense_statement}"
        logger.error(message, exc_info=True)
        raise exceptions.CouldNotLoadSalaryStmtError(message=message) from exc


def load_details_from_all_expense_stmts(
    expense_statements: typing.Iterable[pathlib.Path],
) -> pd.core.frame.DataFrame:
    """
    Load the salary details from an iterable of files.

    Parameters
    ----------
    expense_statements: Iterable[pathlib.Path]
        An iterator having the full path of the salary statements.
    """
    all_salary_statements_concatenated = pd.concat(
        [
            load_details_from_expense_stmt(expense_statement=statement_path)
            for statement_path in expense_statements
        ]
    )
    all_salary_statements_concatenated.sort_values(by=["Value date"], inplace=True)
    all_salary_statements_concatenated.drop_duplicates(inplace=True)
    all_salary_statements_concatenated.reset_index(inplace=True)
    all_salary_statements_concatenated.drop(columns=["index"], inplace=True)
    return all_salary_statements_concatenated


def get_expense_report(
    config_file_path: str, salary_statement_path: str, is_dir: bool = True
) -> expense_viewer.expense.expense.Expense:
    """
    Get the expense report for the month in the salary statement.

    Parameters
    ----------
    config_file_path : str
        The full path of the config yaml file containing the expense rules.
    salary_statement_path : str
        The full path of the csv file containing the salary statement of the month.
    is_dir: bool
        Is the salary statement path a directory of a single path string.
    """
    config_file: pathlib.Path = pathlib.Path(config_file_path)
    salary_statement: pathlib.Path = pathlib.Path(salary_statement_path)
    try:
        config = omegaconf.OmegaConf.load(config_file)
        if is_dir:
            # The salary statements are in a directory
            check_format_of_salary_statement(
                salary_statement_paths=salary_statement.glob("*")
            )
            salary_details = load_details_from_all_expense_stmts(
                expense_statements=salary_statement.glob("*")
            )
        else:
            check_format_of_salary_statement(salary_statement_paths=(salary_statement,))
            salary_details = load_details_from_expense_stmt(
                expense_statement=salary_statement
            )
        expense_obj = expense.OverallExpense(expense=salary_details, config=config)
        expense_obj.add_child_expenses()
        return expense_obj
    except exceptions.Error as exc:
        print(exc)

    assert False  # Again this line should never be reached.
