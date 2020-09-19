# Expense viewer
This is a Python based application which helps in viewing the expenses incurred over a period of months given a salary statement

## Requirements for this application 
1. This application is made to work with a jupyter notebook , hence some knowledge of working with jupyter notebooks is required
2. You would need a expense statement in `csv` format. The application has to parse the csv formatted file and then load into the application for further information extraction.
3. You would need the expense categories rules defined inside the `expense_config.yaml` file.

## Using the application

Below is a small snapshot of how this application can be used:

```
import pathlib

config_file = pathlib.Path("expense_config.yaml")
transactions_file = pathlib.Path("Transactions.csv")

expense = get_expense_report(config_file, transactions_file)
expense.show_expense_summary_graph()
```

This should print a bar chart in which the X axis represents the months for which the expenses were calculated and the Y axis the actual value of expenses.

In order to understand more about the expenses of a single month we can drill down more into individual child objects :

```
import pathlib

config_file = pathlib.Path("expense_config.yaml")
transactions_file = pathlib.Path("Transactions.csv")

expense = get_expense_report(config_file, transactions_file)
expense.child_expenses["May"].show_expense_summary_graph()
```
