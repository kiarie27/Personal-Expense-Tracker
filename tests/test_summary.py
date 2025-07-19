from datetime import date
from click.testing import CliRunner

from commands.summary import summary_cmd
from models.expense import Expense

def _seed(session):
    session.add_all(
        [
            Expense(date=date(2025, 7, 15), category="food", amount=10),
            Expense(date=date(2025, 7, 16), category="food", amount=5),
            Expense(date=date(2025, 7, 17), category="transport", amount=20),
        ]
    )
    session.commit()

def test_summary_totals_and_top(db_session, monkeypatch):
    _seed(db_session)
    monkeypatch.setattr("commands.summary.SessionLocal", lambda: db_session)

    runner = CliRunner()
    res = runner.invoke(summary_cmd, ["-n", "1"])
    assert res.exit_code == 0
 
    assert res.output.count("\n") <= 6
    assert "transport" in res.output
    assert "food" not in res.output