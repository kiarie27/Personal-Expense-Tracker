

"""
init_db.py

Run this script once to (re)initialise the SQLite database **and**
populate it with a handful of sample expenses.  Useful for demos,
screenshots, or for running tests against predictable data.

    pipenv run python init_db.py
"""

from datetime import date

from db.database import Base, engine, SessionLocal
from models.expense import Expense

# ----------------------------------------------------------------------- #
# Sample seed data
# ----------------------------------------------------------------------- #
SEED_EXPENSES = [
    {"date": date(2025, 7, 15), "category": "food",         "amount": 140.00, "description": "Ugali & sukuma wiki"},
    {"date": date(2025, 7, 16), "category": "transport",    "amount":  80.00, "description": "Matatu CBD → Westlands"},
    {"date": date(2025, 7, 17), "category": "mobile_money", "amount":  33.00, "description": "M-Pesa withdrawal fee"},
    {"date": date(2025, 7, 18), "category": "coffee",       "amount": 250.00, "description": "Java House latte"},
    {"date": date(2025, 7, 19), "category": "entertain",    "amount": 600.00, "description": "KICC rooftop ticket"},
]


def reset_database() -> None:
    """Drop (if exists) and recreate the expenses table."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed_data() -> None:
    """Insert the SEED_EXPENSES rows into the DB."""
    session = SessionLocal()
    try:
        for row in SEED_EXPENSES:
            session.add(Expense(**row))
        session.commit()
        print(f"✅ Inserted {len(SEED_EXPENSES)} sample expenses.")
    finally:
        session.close()


if __name__ == "__main__":
    reset_database()
    seed_data()
    print("📂 Database initialised and seeded at expenses.db")