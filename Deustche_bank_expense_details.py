# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: expense
#     language: python
#     name: expense
# ---

# +
# Sample code for Deustche bank expense statements

import pathlib

from expense_viewer import get_expense_report

salary_statement_path = pathlib.Path("./Transactions/Deustche_bank")

config_file = pathlib.Path("./Deutsche_bank_expense_config.yaml")

report = get_expense_report(config_file_path=config_file, salary_statement_path=salary_statement_path, statement_bank="Deutsche Bank")

expense_report = report.get_expenses_report()

expense_report
# -

expense_report["Savings"].sum() / len(expense_report.index)

# ## Gambling

# +
import pandas as pd

data = {"Month": [], "Lottery expense": [], "Winnings": [], "Profit": []}
for month in report.get_child_expense_labels():
    monthly_report = report.child_expenses[month]
    child_expenses_for_month = monthly_report.get_child_expense_labels()
    if "Lottery" in child_expenses_for_month:
        total_expense_on_lottery = monthly_report.child_expenses["Lottery"].expense["Debit"].sum()
        extra_credit_data = monthly_report.expense[monthly_report.expense["Payment Details"].str.contains("Gewinnauszahlung", na=False)]
        data["Winnings"].append(extra_credit_data["Credit"].sum())
        data["Month"].append(month)
        data["Lottery expense"].append(total_expense_on_lottery)
        data["Profit"].append(extra_credit_data["Credit"].sum() - total_expense_on_lottery)

frame = pd.DataFrame.from_dict(data)
average = frame["Profit"].sum() / len(frame.index)
print(f"Average winnings over the time period is : {average}")
frame
# -

report.salary_savings_credit_data_per_month

# ## Function to give you the months of a year in the format MM-YYYY

# +
import calendar
from datetime import datetime

def get_month_year_strings(year):
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    month_year_list = []
    
    # Check if the given year is the current year
    if year == str(current_year):
        # Iterate over months until the current month
        for month in range(1, current_month + 1):
            month_name = calendar.month_name[month]
            month_year_list.append(f"{month_name}-{year}")
    else:
        # If the given year is not the current year, include all months
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            month_year_list.append(f"{month_name}-{year}")
    
    return month_year_list


# -

# ## The amount that we spent on fucking Radio

report.expense[report.expense["Payment Details"].str.contains("Rund", na=False)]

# ## Gambling in any individual month

month = "March-2024"
report.child_expenses[month].child_expenses["Lottery"].expense

# ## Gambling winnings in a month
#

month = "March-2024"
report.child_expenses[month].expense[report.child_expenses[month].expense["Payment Details"].str.contains("Gewinnauszahlung", na=False)]

# ## Property management single month

month = "August-2023"
has_rinp = report.child_expenses[month].expense[report.child_expenses[month].expense["Payment Details"].str.contains("RINP", na=False)]
has_rinp[has_rinp["Payment Details"].str.contains("Subhayan", na=False)]

# ## Property management whole year

# +
import pandas as pd

all_dataframes = []
year = "2024"
for month in get_month_year_strings(year):
    all_dataframes.append(report.child_expenses[month].expense[report.child_expenses[month].expense["Beneficiary / Originator"].str.contains("DWS Grundbesitz GmbH", na=False)])

pd.concat(all_dataframes)
# -

# ## How much have i paid to translator

report.expense[report.expense["Beneficiary / Originator"].str.contains("Anne", na=False)]

# ## whatever Dauerauftrag means(standing order)

month = "February-2024"
report.child_expenses[month].expense[report.child_expenses[month].expense["Payment Details"].str.contains("Dauerauftrag", na=False)]

# ## Just see the expense of a month

month = "March-2024"
report.child_expenses[month].expense

report.expense.dtypes

get_month_year_strings("2024")


