


import click
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from db.database import SessionLocal
from models.expense import Expense

# ----------------------------------------------------------------------- #
# Helper functions
# ----------------------------------------------------------------------- #
def _parse_date(value: str) -> date:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise click.BadParameter("Date must be in YYYY-MM-DD format.") from exc

    if parsed > date.today():
        raise click.BadParameter("Date cannot be in the future.")
    return parsed


def _validate_amount(value: str) -> Decimal:
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise click.BadParameter("Amount must be a valid number.") from exc

    if amount <= 0:
        raise click.BadParameter("Amount must be greater than zero.")
    return amount


# ----------------------------------------------------------------------- #
# Additional helper
# ----------------------------------------------------------------------- #
def _validate_category(value: str) -> str:
    """Strip and validate a category (1–50 chars)."""
    value = value.strip()
    if not value:
        raise click.BadParameter("Category cannot be empty.")
    if len(value) > 50:
        raise click.BadParameter("Category must be 50 characters or fewer.")
    return value


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
    prompt="Optional description",
    default="",
    show_default=False,
    help="Optional description (press Enter to skip).",
)
def add_expense_cmd(date_str: str, category: str, amount: str, description: str):

    # Validate inputs ---------------------------------------------------- #
    date_obj = _parse_date(date_str)
    amount_val = _validate_amount(amount)
    category = _validate_category(category)
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


# Export helpers
__all__ = ["_parse_date", "_validate_amount", "_validate_category"]