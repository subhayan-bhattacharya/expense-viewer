# Expense viewer
This is a Python based application which helps in viewing the expenses incurred over a period of months given a salary statement

## Requirements for this application 
1. This application is made to work with a jupyter notebook , hence some knowledge of working with jupyter notebooks is required
2. You would need all expense statements in `csv` format. The application has to parse the csv formatted files and then load into the application for further information extraction.
3. You would need the expense categories rules defined inside the `expense_config.yaml` file.

## Using the application

Below is a small snapshot of how this application can be used:

```
import pathlib
from expense_viewer import get_expense_report

config_file = "expense_config.yaml"
transactions_dir = "/home/user/expenses/Transactions"
bank = "Deutsche Bank"

expense = get_expense_report(config_file, transactions_dir, bank)
expense.get_expenses_report()
```

In order to understand more about the expenses of a single month we can drill down more into individual child objects :

```
import pathlib
from expense_viewer import get_expense_report

config_file = "expense_config.yaml"
transactions_dir = "/home/user/expenses/Transactions"
bank = "Deutsche Bank"

expense = get_expense_report(config_file, transactions_dir, bank)
expense_months = expense.get_child_expense_labels()
october = expense.child_expenses["October"]
october.expense
```
