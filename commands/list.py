

import click
from datetime import datetime, date
from typing import Optional

from tabulate import tabulate

from db.database import SessionLocal
from models.expense import Expense


def _parse_date_opt(value: Optional[str], flag: str) -> Optional[date]:
    """Parse an optional YYYY-MM-DD string into a `date` or return None."""
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise click.BadParameter(f"{flag} must be in YYYY-MM-DD format.") from exc



@click.command(help="List expenses, with optional category and date filters.")
@click.option(
    "--category",
    "-c",
    help="Filter by category (case-insensitive).",
)
@click.option(
    "--from-date",
    "-f",
    "from_date_str",
    help="Start date (YYYY-MM-DD).",
)
@click.option(
    "--to-date",
    "-t",
    "to_date_str",
    help="End date (YYYY-MM-DD).",
)
def list_expenses_cmd(category: Optional[str], from_date_str: Optional[str], to_date_str: Optional[str]):
    """Callback for the `list` command."""

    from_date = _parse_date_opt(from_date_str, "--from-date")
    to_date = _parse_date_opt(to_date_str, "--to-date")

    if from_date and to_date and from_date > to_date:
        raise click.BadParameter("--from-date cannot be after --to-date.")


    db = SessionLocal()
    try:
        q = db.query(Expense)

        if category:
            q = q.filter(Expense.category.ilike(category))  # case-insensitive match

        if from_date:
            q = q.filter(Expense.date >= from_date)
        if to_date:
            q = q.filter(Expense.date <= to_date)

        rows = q.order_by(Expense.date.desc(), Expense.id.desc()).all()

        # 3) Display ----------------------------------------------------- #
        if not rows:
            click.echo("No matching expenses.")
            return

        table = [
            [
                e.id,
                e.date.isoformat(),
                e.category,
                f"{e.amount:.2f}",
                (e.description or ""),
            ]
            for e in rows
        ]
        click.echo(
            tabulate(table, headers=["ID", "Date", "Category", "Amount", "Description"])
        )
    finally:
        db.close()