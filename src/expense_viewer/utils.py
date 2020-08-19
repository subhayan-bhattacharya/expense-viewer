"""File which has the common utility functions inside the project."""

import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

    result_dataframe = data[pd.eval(condition_str)]

    return list(result_dataframe.index.values)


def get_expense_month(expense: pd.DataFrame) -> str:
    """Get the expense month from the data."""
    expense_copy = expense.copy()

    months = expense_copy["Value date"].dt.month

    most_frequent_month_int = months.value_counts().idxmax()

    # Convert the month number(1/2) into a month string(January/February etc)
    return datetime.date(1900, most_frequent_month_int, 1).strftime("%B")


def display_bar_charts(
    labels: List[str], axes_labels: List[str], **data_to_plot
) -> None:
    """Display grouped bar charts with annotations using matoplotlib."""
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    _, ax = plt.subplots()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                "{}".format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    for data in data_to_plot:
        rects = ax.bar(x, data_to_plot[data], width, label=data)
        autolabel(rects)
        x = [y + width for y in x]

    ax.set_ylabel(axes_labels[1])
    ax.set_xlabel(axes_labels[0])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()

