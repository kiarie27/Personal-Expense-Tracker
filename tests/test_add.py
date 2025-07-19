from datetime import date
from click.testing import CliRunner

from commands.add import add_expense_cmd
from models.expense import Expense

def test_add_happy_path(db_session, monkeypatch):
    runner = CliRunner()

  
    monkeypatch.setattr("commands.add.SessionLocal", lambda: db_session)

    result = runner.invoke(
        add_expense_cmd,
        ["-d", "2025-07-20", "-c", "food", "-a", "10.5", "-desc", "Tacos"],
    )
    assert result.exit_code == 0
    assert "✅" in result.output

    row = db_session.query(Expense).one()
    assert row.date == date(2025, 7, 20)
    assert row.category == "food"
    assert row.amount == 10.5
    assert row.description == "Tacos"


def test_add_rejects_negative_amount(db_session, monkeypatch):
    monkeypatch.setattr("commands.add.SessionLocal", lambda: db_session)
    runner = CliRunner()
    res = runner.invoke(add_expense_cmd, ["-c", "misc", "-a", "-3"])
    assert res.exit_code != 0
    assert "greater than zero" in res.output