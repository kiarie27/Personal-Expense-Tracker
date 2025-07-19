

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL. The file will be created in the project root if it
# doesn’t already exist.
DATABASE_URL = "sqlite:///expenses.db"

# Create the SQLAlchemy engine.
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for verbose SQL logging during debugging
    connect_args={"check_same_thread": False},  # Needed for SQLite & threading
)

# Session factory we’ll use throughout the app.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for our ORM models.
Base = declarative_base()