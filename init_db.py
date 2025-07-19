

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
    #  id |     date     |  category   | amount |  description
    {"date": date(2025, 7, 15), "category": "food",      "amount": 12.50, "description": "Lunch burrito"},
    {"date": date(2025, 7, 16), "category": "transport", "amount":  3.40, "description": "Bus fare"},
    {"date": date(2025, 7, 17), "category": "groceries", "amount": 32.10, "description": "Weekly veggies"},
    {"date": date(2025, 7, 18), "category": "entertain", "amount": 15.00, "description": "Movie night"},
    {"date": date(2025, 7, 19), "category": "coffee",    "amount":  2.80, "description": "Flat white"},
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