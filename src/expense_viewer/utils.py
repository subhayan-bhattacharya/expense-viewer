"""File which has the common utility functions inside the project."""

from os import confstr
import pandas as pd
from typing import Any, Dict, List


def get_full_condition_string(
    condition: Dict[str, Any], dataframe_prefix: str = "data"
) -> str:
    """Construct a condition string using the condition dict."""
    identifiers = condition["identifiers"]
    logical_operator = condition["logical_operator"]

    identifier_strs = []

    for identifier in identifiers:
        column_name_str = f"{'data'}[\"{identifier['column']}\"]"

        value = identifier["value"]

        comparison_operator = identifier["comparison_operator"]
        if comparison_operator == "contains":
            identifier_strs.append(f'{column_name_str}.str.contains("{value}")')
        else:
            operator = f" {comparison_operator} "
            identifier_strs.append(f"{column_name_str}{operator}{value}")

    if logical_operator == "OR":
        return " | ".join(identifier_strs)
    elif logical_operator == "AND":
        return " & ".join(identifier_strs)


def get_row_index_for_matching_columns(
    condition: Dict[str, Any], data: pd.DataFrame
) -> List[int]:
    """Get the row index for columns matching the condition in the dataframe."""
    condition_str = get_full_condition_string(condition)
    print(f"Got back the condition string as : {condition_str}")

    result_dataframe = data[pd.eval(condition_str)]

    return list(result_dataframe.index.values)
