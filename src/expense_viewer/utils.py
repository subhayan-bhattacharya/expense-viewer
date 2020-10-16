"""File which has the common utility functions inside the project."""
import calendar
import datetime
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def get_expense_month(expense: pd.DataFrame) -> str:
    """Get the expense month from the data."""
    expense_copy = expense.copy()

    months = expense_copy["Value date"].dt.month

    most_frequent_month_int = months.value_counts().idxmax()

    # Convert the month number(1/2) into a month string(January/February etc)
    return datetime.date(1900, most_frequent_month_int, 1).strftime("%B")


def get_next_month_label(month: str) -> str:
    """Get the next month of the month supplied as input."""
    datetime_object = datetime.datetime.strptime(month, "%B")

    next_month_num = calendar.nextmonth(  # type: ignore
        datetime.datetime.now().year, datetime_object.month
    )[1]
    return datetime.date(1900, next_month_num, 1).strftime("%B")


def display_bar_charts(
    labels: List[str], axes_labels: List[str], **data_to_plot
) -> None:
    """Display grouped bar charts with annotations using matplotlib."""
    x = np.arange(len(labels))  # the label locations
    width = 0.3  # the width of the bars

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

    x_loc = x

    for data in data_to_plot:
        rects = ax.bar(x_loc, data_to_plot[data], width, label=data)
        autolabel(rects)
        x_loc = [y + width for y in x_loc]

    ax.set_ylabel(axes_labels[1])
    ax.set_xlabel(axes_labels[0])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.ylim(0, 5000)
    plt.show()


def display_pie_charts(labels: List[str], expenses: List[float]) -> None:
    """Display pie charts using the data provided."""

    def absolute_value(val):
        """Get absolute value in a pie chart."""
        a = np.round(val / 100.0 * sum(expenses), 2)
        return a

    explode = tuple([0] * len(labels))
    fig1, ax1 = plt.subplots()
    ax1.pie(
        expenses,
        explode=explode,
        labels=labels,
        autopct=absolute_value,
        shadow=True,
        startangle=90,
    )
    ax1.axis("equal")
    plt.show()
