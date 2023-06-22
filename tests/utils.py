import pytest
from app.repository.connection import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import load_environment_variables, get_db_uri

load_environment_variables()

test_engine = create_engine(
    get_db_uri(with_driver=True, test=True),
    echo=True
)

TestSession = sessionmaker(test_engine)
"""
Attempt to copy data from actual DB into test DB
upon running tests:

CREATE DATABASE test_nostar TEMPLATE nostar;
"""
@pytest.fixture(scope="module")
def db_session():
    # TODO Assuming Test DB is populated by Alembic revisions
    # in CI pipeline or, using a 100% rolled-back session to the
    # actual database for the environment.
    session = Session()
    yield session
    # Cleanup
    session.rollback()
    session.close()

