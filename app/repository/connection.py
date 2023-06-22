from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import load_environment_variables, get_db_uri
# Load Environment TODO this may be redundant
load_environment_variables()
# Engine
engine = create_engine(
    get_db_uri(with_driver=True),
    echo=True
)
# Currently being distributed to app
# for DB connectivity.
Session = sessionmaker(engine)

# Not currently used
def _yield_db_session():
    session = Session()
    yield session
    # Close
    session.close()
