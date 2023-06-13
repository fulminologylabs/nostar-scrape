from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import load_environment_variables, get_db_uri

load_environment_variables()

engine = create_engine(
    get_db_uri(with_driver=True),
    echo=True
)

Session = sessionmaker(engine)