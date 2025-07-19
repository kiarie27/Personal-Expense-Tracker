

"""
Click command: `tracker.py summary`

Provides a quick spending summary, grouped by category.  You can narrow the
data set to a single month and/or limit the output to the top‑N categories.

Examples
--------
    # Overall totals per category
    pipenv run tracker summary

    # Totals for July 2025 only
    pipenv run tracker summary -m 2025-07

    # Show just the five biggest categories (all time)
    pipenv run tracker summary -n 5

    # Top‑3 categories for July 2025
    pipenv run tracker summary -m 2025-07 -n 3
"""

import click
from datetime import datetime, date
import calendar
import re
from typing import Optional

from sqlalchemy import func
from tabulate import tabulate

from db.database import SessionLocal
from models.expense import Expense

# ----------------------------------------------------------------------- #
# Helper utilities
# ----------------------------------------------------------------------- #
def _validate_month(month_str: Optional[str]) -> Optional[str]:
    """
    Accepts either:
    • `'YYYY-MM'` (e.g. `2025-07`) – returned unchanged.
    • A month name or 3‑letter abbreviation (`'July'`, `'Jul'`, case‑insensitive) –
      converted to the current year as `'YYYY-MM'`.
    """
    if month_str is None:
        return None

    # Already YYYY-MM?
    if re.fullmatch(r"\d{4}-\d{2}", month_str):
        return month_str

    # Try full / abbreviated month names
    month_lower = month_str.lower()
    for i in range(1, 13):
        if (
            calendar.month_name[i].lower() == month_lower
            or calendar.month_abbr[i].lower() == month_lower
        ):
            return f"{date.today().year}-{i:02d}"

    raise click.BadParameter(
        "--month must be in YYYY-MM format or a month name like 'July'."
    )


# ----------------------------------------------------------------------- #
# Click command
# ----------------------------------------------------------------------- #
@click.command(help="Summarize spending totals, grouped by category.")
@click.option(
    "--month",
    "-m",
    help="Restrict to a single month (YYYY-MM or month name).",
)
@click.option(
    "--top",
    "-n",
    type=int,
    help="Show only the top‑N categories (by total spent).",
)
def summary_cmd(month: Optional[str], top: Optional[int]):
    """Callback for the `summary` command."""
    month = _validate_month(month)
    if top is not None and top <= 0:
        raise click.BadParameter("--top must be a positive integer.")

    db = SessionLocal()
    try:
        # ---------------------------------------------------------------- #
        # Build the aggregate query
        # ---------------------------------------------------------------- #
        q = db.query(
            Expense.category.label("category"),
            func.sum(Expense.amount).label("total"),
        )

        if month:
            # Filter rows to the given month.
            q = q.filter(func.strftime("%Y-%m", Expense.date) == month)

        q = q.group_by(Expense.category).order_by(func.sum(Expense.amount).desc())

        if top:
            q = q.limit(top)

        rows = q.all()
        if not rows:
            click.echo("No matching expenses.")
            return

        # ---------------------------------------------------------------- #
        # Display table with a grand total
        # ---------------------------------------------------------------- #
        grand_total = sum(r.total for r in rows)
        table = [[idx + 1, r.category, f"{r.total:.2f}"] for idx, r in enumerate(rows)]

        click.echo(
            tabulate(
                table,
                headers=["#", "Category", "Total"],
                floatfmt=".2f",
                colalign=("right", "left", "right"),
            )
        )
        click.secho(f"\nGrand total: {grand_total:.2f}", fg="cyan")

        # Highlight the single biggest category
        top_row = rows[0]
        click.secho(
            f"Highest spending category: {top_row.category} "
            f"({top_row.total:.2f})",
            fg="yellow",
        )
    finally:
        db.close()