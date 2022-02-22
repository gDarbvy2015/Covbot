from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from lib.database.database_manager import DatabaseManager
from lib.database.entities import Vaccination, Case
from lib.database.querier import Querier


@pytest.fixture(scope="session")
def db_manager(request):
    db_manager = DatabaseManager("covbot_test")
    db_manager.create_database()
    db_manager.create_tables()
    print("Setting up")
    yield db_manager
    print("Tearing down")
    db_manager.drop_tables()


@pytest.fixture(scope="session")
def session(db_manager: DatabaseManager):
    session = Session(db_manager.engine)
    yield session
    session.rollback()


@pytest.fixture(scope="session")
def querier(db_manager, session):
    return Querier("covbot_test", db_manager, session)

def test_hi(session, querier):
    case = Case(id=3, date=datetime.now().date(), country="Austria", country_normalized="austria", cases=1000, cumulative_cases=1000)
    session.add(case)

def test_two(db_manager):
    print("Bye")