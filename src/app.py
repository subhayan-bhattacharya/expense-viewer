import pathlib

import omegaconf
import streamlit

import expense_viewer


def run_streamlet_app():
    project_dir = pathlib.Path(__file__).parent.parent
    config_file = project_dir / "expense_config.yaml"
    transactions_dir = project_dir / "Transactions"

    config = omegaconf.OmegaConf.load(config_file)
    expense_viewer.main.check_format_of_salary_statement(
        salary_statement_paths=transactions_dir.glob("*")
    )
    salary_details = expense_viewer.main.load_details_from_all_expense_stmts(
        expense_statements=transactions_dir.glob("*")
    )
    expense_obj = expense_viewer.expense.overall_expense.OverallExpense(
        expense=salary_details, config=config
    )
    expense_obj.add_child_expenses()
    streamlit.bar_chart(
        data=expense_obj.get_expense_summary_dataframe(), use_container_width=True
    )


if __name__ == "__main__":
    run_streamlet_app()
