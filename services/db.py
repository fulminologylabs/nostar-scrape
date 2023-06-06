from repository.models import Relay, Base, RelayConfig, Job, \
    Batch, JobType, EventKind, TextNote, Filter, Subscription
from repository.connection import engine
from utils import load_environment_variables, get_db_uri
from sqlalchemy.orm import Session


class DBService:
    def __init__(self):
        #load_environment_variables()
        #self._db_uri = get_db_uri(with_driver=True)
        self.session = Session(bind=engine)
    


