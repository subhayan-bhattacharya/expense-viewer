import logging
import pathlib
import typing

import pandas as pd
import ruamel.yaml

import expense_viewer.exceptions as exceptions
import expense_viewer.expense.overall_expense as expense

EXPECTED_FORMATS = (".csv",)

logger = logging.getLogger(__name__)


def replace_comma_if_string(value: typing.Union[str, float]):
    """Check if the value is a string then do replacement of comma."""
    if isinstance(value, str):
        return value.replace(",", "")
    return value


def read_yaml_file_contents(yaml_file_path: pathlib.Path) -> typing.Dict:
    """
    Read a yaml file and return the contents.

    Parameters
    ----------
    yaml_file_path:
        Full path of the yaml file to be read

    Returns
    -------
    typing.Dict
        The contents of the yaml file as a dict

    Raises
    ------
    CouldNotLoadYamlFile
        When the yaml file could not be found for reading
    """
    logger.debug(f"Read contents of yaml file {yaml_file_path}")

    try:
        yaml = ruamel.yaml.YAML()
        with open(yaml_file_path, "r") as stream:
            contents = yaml.load(stream)
        return contents
    except Exception as exc:
        message = f"Could not read yaml file..{yaml_file_path}"
        logger.error(f"{message}", exc_info=True)
        raise exceptions.CouldNotLoadYamlFileError(message=message) from exc


def check_format_of_salary_statement(salary_statement_path: pathlib.Path) -> None:
    """
    Check that the format of salary statement is in the right format.

    Parameters
    ----------
    salary_statement_path : pathlib.Path
        The salary statement file full path

    Raises
    ------
    WrongFormatError
        When the format of the salary statement is not right
    """
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
        "Value date",
    ]

    try:
        transactions = pd.read_csv(
            expense_statement,
            encoding="latin",
            error_bad_lines=False,
            skiprows=4,
            delimiter=";",
            usecols=columns_to_use,
            parse_dates=["Value date"],
        )
        transactions.drop(transactions.tail(1).index, inplace=True)
        transactions["Credit"] = transactions["Credit"].apply(replace_comma_if_string)
        transactions["Debit"] = transactions["Debit"].apply(replace_comma_if_string)
        transactions["Credit"] = transactions["Credit"].astype("float64")
        transactions["Debit"] = transactions["Debit"].astype("float64")
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


def get_expense_report(config_file_path: str, salary_statement_path: str) -> None:
    """
    Get the expense report for the month in the salary statement.

    Parameters
    ----------
    config_file_path : str
        The full path of the config yaml file containing the expense rules.
    salary_statement_path : str
        The full path of the csv file containing the salary statement of the month.
    """
    config_file = pathlib.Path(config_file_path)
    salary_statement = pathlib.Path(salary_statement_path)
    try:
        config = read_yaml_file_contents(config_file)
        check_format_of_salary_statement(salary_statement_path=salary_statement)
        salary_details = load_details_from_expense_stmt(
            expense_statement=salary_statement
        )
        expense_obj = expense.OverallExpense(expense=salary_details, config=config)
        expense_obj.add_child_expenses()
        return expense_obj
    except exceptions.Error as exc:
        print(exc)
