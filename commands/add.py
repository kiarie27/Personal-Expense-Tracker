

"""
Click command: `tracker.py add`

Adds a single expense row into the `expenses` table.

Usage examples:

    # Defaults date to today
    pipenv run tracker add -c food -a 12.50 -desc "Lunch"

    # Explicit date
    pipenv run tracker add --date 2025-07-18 --category transport --amount 3.40

The command can also be invoked programmatically from the interactive menu
via `add_expense_cmd.main(standalone_mode=False)`.
"""
import click
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from db.database import SessionLocal
from models.expense import Expense

# ----------------------------------------------------------------------- #
# Helper functions
# ----------------------------------------------------------------------- #
def _parse_date(value: str) -> date:
    """Return a `date` object parsed from YYYY-MM-DD string."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise click.BadParameter("Date must be in YYYY-MM-DD format.") from exc


def _validate_amount(value: str) -> Decimal:
    """Ensure the amount is a positive decimal number."""
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise click.BadParameter("Amount must be a valid number.") from exc

    if amount <= 0:
        raise click.BadParameter("Amount must be greater than zero.")
    return amount


# ----------------------------------------------------------------------- #
# Click command
# ----------------------------------------------------------------------- #
@click.command(help="Add a new expense record.")
@click.option(
    "--date",
    "-d",
    "date_str",
    default=lambda: str(date.today()),
    help="Expense date in YYYY-MM-DD. Defaults to today.",
    show_default="today",
)
@click.option("--category", "-c", prompt=True, help="Expense category.")
@click.option(
    "--amount",
    "-a",
    prompt=True,
    help="Amount spent.",
)
@click.option(
    "--description",
    "-desc",
    default="",
    help="Optional description.",
)
def add_expense_cmd(date_str: str, category: str, amount: str, description: str):
    """Callback for the `add` command."""
    # Validate inputs ---------------------------------------------------- #
    date_obj = _parse_date(date_str)
    amount_val = _validate_amount(amount)
    category = category.strip()
    description = description.strip()

    # Persist to DB ------------------------------------------------------ #
    db = SessionLocal()
    try:
        expense = Expense(
            date=date_obj,
            category=category,
            amount=float(amount_val),
            description=description or None,
        )
        db.add(expense)
        db.commit()
        click.secho(f"✅ Saved: {expense}", fg="green")
    except Exception as exc:
        db.rollback()
        click.secho(f"❌ Failed to save expense: {exc}", fg="red")
    finally:
        db.close()