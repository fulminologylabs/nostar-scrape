from repository.models import Relay, Base, RelayConfig, Job, \
    Batch, JobType, EventKind, TextNote, Filter, Subscription
from repository.connection import engine
from utils import load_environment_variables, get_db_uri
from sqlalchemy.orm import Session
from sqlalchemy import select

class DBService:
    def __init__(self):
        #load_environment_variables()
        #self._db_uri = get_db_uri(with_driver=True)
        self.session = Session(bind=engine)
    
    def select_relay_by_id(self, relay_id: int) -> Relay:
        sql = select(Relay).where(Relay.id == relay_id)
        result = self.session.scalars(sql)
        return result
    
    def select_all_relays(self) -> list[Relay]:
        relays = self.session.query(Relay).all()
        return relays

