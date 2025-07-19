from datetime import date
from click.testing import CliRunner

from commands.list import list_expenses_cmd
from models.expense import Expense

def _seed(session):
    session.add_all(
        [
            Expense(date=date(2025, 7, 10), category="food", amount=5),
            Expense(date=date(2025, 7, 12), category="transport", amount=3),
            Expense(date=date(2025, 8,  1), category="food", amount=7),
        ]
    )
    session.commit()

def test_list_filters_by_category(db_session, monkeypatch):
    _seed(db_session)
    monkeypatch.setattr("commands.list.SessionLocal", lambda: db_session)

    runner = CliRunner()
    res = runner.invoke(list_expenses_cmd, ["-c", "food"])
    assert res.exit_code == 0
    assert res.output.count("food") == 2
    assert "transport" not in res.output

def test_list_date_range(db_session, monkeypatch):
    _seed(db_session)
    monkeypatch.setattr("commands.list.SessionLocal", lambda: db_session)

    runner = CliRunner()
    res = runner.invoke(list_expenses_cmd, ["-f", "2025-07-11", "-t", "2025-07-31"])
    assert res.exit_code == 0
    assert "transport" in res.output          # 12 Jul row
    assert "2025-08" not in res.output        # 1 Aug excluded