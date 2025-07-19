import sys
from pathlib import Path


root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import os
import tempfile
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from models.expense import Expense

@pytest.fixture(scope="function")
def db_session():
    """Yield a fresh Session connected to a temp SQLite DB."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)                # we only need the filename
    engine = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    # Build schema
    Base.metadata.create_all(bind=engine)

    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        os.remove(path)