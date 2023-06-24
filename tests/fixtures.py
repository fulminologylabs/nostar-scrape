import pytest
import string
import random
from datetime import datetime
from app.services.admin import Admin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.repository.models import Base
from app.utils import load_environment_variables, get_test_db_uri,\
    default_relay_config_epoch_start

load_environment_variables()

test_engine = create_engine(
    get_test_db_uri(
        with_driver=True, 
    ),
    echo=True
)

TestSession = sessionmaker(test_engine)

@pytest.fixture(scope="module")
def db_session():
    # TODO Assuming Test DB is populated by Alembic revisions
    # in CI pipeline or, using a 100% rolled-back session to the
    # actual database for the environment.
    session = TestSession()
    yield session
    # Cleanup
    #session.rollback()
    session.close()

@pytest.fixture(scope="module")
def relay_url(str_len: int = 7) -> str:
    """
        TODO should at some point respect url validation
    """
    res = "".join(random.choices(
        string.ascii_lowercase + string.digits,
        k=str_len
    ))
    return res

@pytest.fixture(scope="module")
def relay_name(str_len: int = 7) -> str:
    """
        Intentionally redundant to relay_url
        as they will diverge with iteration.
    """
    res = "".join(random.choices(
        string.ascii_lowercase + string.digits,
        k=str_len
    ))
    return res

@pytest.fixture
def dt_epoch_start() -> datetime:
    return default_relay_config_epoch_start()

@pytest.fixture(scope="module")
def admin(db_session):
    return Admin(db_session=db_session)
