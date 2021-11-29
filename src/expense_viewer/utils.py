"""File which has the common utility functions inside the project."""
import datetime
from typing import Any, Dict, List

import pandas as pd
from dateutil.relativedelta import relativedelta


def get_full_condition_string(condition: Dict[str, Any]) -> str:
    """Construct a condition string using the condition dict."""
    identifiers = condition["identifiers"]
    logical_operator = condition["logical_operator"]

    identifier_strs = []

    for identifier in identifiers:
        identifier_strs.append(
            get_condition_str_for_single_identifier(identifier=identifier)
        )

    if logical_operator == "OR":
        return " | ".join(identifier_strs)
    elif logical_operator == "AND":
        return " & ".join(identifier_strs)

    assert False  # This line should never be reached .


def get_condition_str_for_single_identifier(
    identifier: Dict[str, Any], dataframe_prefix: str = "data"
) -> str:
    """Get the condition str for a single identifier."""
    column_name_str = f"{dataframe_prefix}[\"{identifier['column']}\"]"

    value = identifier["value"]

    comparison_operator = identifier["comparison_operator"]

    if comparison_operator == "contains":
        return f'{column_name_str}.str.contains("{value}")'
    else:
        operator = f" {comparison_operator} "
        return (
            f"{column_name_str}{operator}{value}"
            if not isinstance(value, str)
            else f"{column_name_str}{operator}'{value}'"
        )


def break_up_dataframe_in_chunks(data: pd.DataFrame, indices: List[int]):
    """Divide a dataframe into chunks as per supplied indexes."""
    start_index = 0
    for index in indices:
        yield data[start_index:index]
        start_index = index + 1
    yield data[start_index:]


def get_row_index_for_matching_columns(
    condition: Dict[str, Any], data: pd.DataFrame
) -> List[int]:
    """Get the row index for columns matching the condition."""
    condition_str = get_full_condition_string(condition)

    result_dataframe = data[pd.eval(condition_str)]

    return list(result_dataframe.index.values)


def get_expense_month_year(expense: pd.DataFrame) -> str:
    """Get the expense month from the data."""
    expense_copy = expense.copy()

    months = expense_copy["Value date"].dt.month
    year = expense_copy["Value date"].dt.year

    most_frequent_month_int = months.value_counts().idxmax()
    most_frequent_month_year = year.value_counts().idxmax()

    most_frequent_month_str = datetime.date(1900, most_frequent_month_int, 1).strftime(
        "%B"
    )
    # Convert the month number(1/2) into a month string(January/February etc)
    return f"{most_frequent_month_str}-{most_frequent_month_year}"


def get_next_month_label(month_year_label: str) -> str:
    """Get the next month of the month supplied as input."""
    datetime_object = datetime.datetime.strptime(month_year_label, "%B-%Y")
    next_month = datetime_object + relativedelta(months=1)
    return next_month.strftime('%B-%Y')
