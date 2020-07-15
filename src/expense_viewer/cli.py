from sys import path
import fire
import pathlib
import logging


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
    try:
        config_file_full_path = pathlib.Path(config_file_path).resolve(strict=True)
        salary_statement_full_path = pathlib.Path(salary_statement_path).resolve(
            strict=True
        )
    except FileNotFoundError as exception:
        logging.error(f"{exception.exc_info}")
    else:
        print("The file could be loaded")


def main():
    fire.Fire(get_expense_report)
