from os import path
from pathlib import PosixPath
import typing
import pathlib
import logging
import ruamel.yaml
import expense_viewer.exceptions as exceptions

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
file_handler = logging.FileHandler("expense_viewer.log")
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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
    FileNotFoundError
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
        raise exceptions.Error(message=message)


def load_config(config_path: pathlib.Path) -> typing.Dict:
    """Load config file and give back contents."""
    if not config_path.is_file():
        message = f"File {config_path} does not exist."
        logger.error(f"{message}")
        raise exceptions.FileOrDirectoryNotFound(message=message)

    return read_yaml_file_contents(config_path)


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
        config = load_config(config_file)
        logger.info(config)
    except exceptions.Error as exc:
        print(exc)
