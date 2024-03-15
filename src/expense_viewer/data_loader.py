import logging
import pathlib
import typing

import pandas as pd

import expense_viewer.exceptions as exceptions

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


def _data_loader_revolut(expense_statement: pathlib.Path) -> pd.core.frame.DataFrame:
    """
    Load the expense details from revolut bank csv file.

    Parameters
    ----------
    expense_statement : pathlib.Path
        The expense statement full path as a csv file
    """
    columns_to_use = ["Type", "Completed Date", "Description", "Amount"]

    try:
        transactions = pd.read_csv(expense_statement, usecols=columns_to_use)
        renamed_transactions = transactions.rename(
            columns={
                "Completed Date": "Value date",
                "Description": "Payment Details",
                "Type": "Transaction Type",
                "Amount": "Credit",
            }
        )
        renamed_transactions["Value date"] = renamed_transactions["Value date"].astype(
            "datetime64"
        )
        renamed_transactions["Value date"] = pd.to_datetime(
            renamed_transactions["Value date"].dt.strftime("%Y-%m-%d")
        )
        renamed_transactions["Credit"] = renamed_transactions["Credit"].astype(
            "float64"
        )
        renamed_transactions["Debit"] = 0.0
        renamed_transactions.loc[renamed_transactions["Credit"] < 0.0, "Debit"] = (
            renamed_transactions["Credit"] * -1
        )
        renamed_transactions.loc[renamed_transactions["Credit"] < 0.0, "Credit"] = 0.0
        return renamed_transactions
    except Exception as exc:
        message = f"Could not load the details from {expense_statement}"
        logger.error(message, exc_info=True)
        raise exceptions.CouldNotLoadSalaryStmtError(message=message) from exc


def _data_loader_deutsche_bank(
    expense_statement: pathlib.Path,
) -> pd.core.frame.DataFrame:
    """
    Load the expense details from deutsche bank csv file.

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
        "Value date",
        "Beneficiary / Originator",
        "IBAN"
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


def load_data_from_all_expense_stmts(
    expense_statements: typing.Iterable[pathlib.Path], callable: typing.Callable
) -> pd.core.frame.DataFrame:
    """
    Load the salary details from an iterable of files.

    Parameters
    ----------
    expense_statements: Iterable[pathlib.Path]
        An iterator having the full path of the salary statements.
    callable: Callable
        The callable to use for loading the expense statement.
    """
    all_salary_statements_concatenated = pd.concat(
        [
            callable(expense_statement=statement_path)
            for statement_path in expense_statements
        ]
    )
    all_salary_statements_concatenated.sort_values(by=["Value date"], inplace=True)
    all_salary_statements_concatenated.drop_duplicates(inplace=True)
    all_salary_statements_concatenated.reset_index(inplace=True)
    all_salary_statements_concatenated.drop(columns=["index"], inplace=True)
    return all_salary_statements_concatenated


BANK_NAME_TO_CALLABLE: typing.Dict[str, typing.Callable] = {
    "Revolut": _data_loader_revolut,
    "Deutsche Bank": _data_loader_deutsche_bank,
}
