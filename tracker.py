#!/usr/bin/env python
"""
CLI entry‑point for the Personal Expense Tracker.

• Run `pipenv run tracker` (no arguments) for an interactive menu.
• Or run sub‑commands directly, e.g. `pipenv run tracker add --help`.
"""
import click
from db.database import Base, engine
from commands.add import add_expense_cmd
from commands.list import list_expenses_cmd
from commands.summary import summary_cmd

# ----------------------------------------------------------------------- #
# Ensure database tables exist on first run
# ----------------------------------------------------------------------- #
Base.metadata.create_all(bind=engine)

# ----------------------------------------------------------------------- #
# Interactive menu helper
# ----------------------------------------------------------------------- #
def interactive_menu() -> None:
    """Simple text menu that re‑uses the Click sub‑commands."""
    while True:
        click.echo("\n===== Personal Expense Tracker =====")
        click.echo("1) Add expense")
        click.echo("2) List expenses")
        click.echo("3) Summary")
        click.echo("4) Exit")

        try:
            choice = int(click.prompt("Select an option", type=int))
        except click.Abort:
            # User hit Ctrl‑C – exit cleanly
            click.echo("\nAborted.")
            return

        if choice == 1:
            add_expense_cmd.main(standalone_mode=False)
        elif choice == 2:
            list_expenses_cmd.main(standalone_mode=False)
        elif choice == 3:
            summary_cmd.main(standalone_mode=False)
        elif choice == 4:
            click.echo("Goodbye!")
            break
        else:
            click.echo("Invalid choice — try again.")

# ----------------------------------------------------------------------- #
# Click root command
# ----------------------------------------------------------------------- #
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Personal Expense Tracker CLI.

    If no sub‑command is provided, drops into an interactive menu.
    """
    if ctx.invoked_subcommand is None:
        interactive_menu()

# Register sub‑commands so they work as `tracker.py add`, etc.
cli.add_command(add_expense_cmd, name="add")
cli.add_command(list_expenses_cmd, name="list")
cli.add_command(summary_cmd, name="summary")

if __name__ == "__main__":
    cli()
