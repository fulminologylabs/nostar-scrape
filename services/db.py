from repository.models import Relay, Base, RelayConfig, Job, \
    Batch, JobType, EventKind, TextNote, Filter, Subscription
from repository.connection import engine, Session
from utils import load_environment_variables, get_db_uri
from sqlalchemy.orm import Session as _Session
from sqlalchemy import select
# For help with developing new queries: https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
# For help with updating / deleting using the DB Models see below for help:
# https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire
class DBService:
    def __init__(self):
        #load_environment_variables()
        #self._db_uri = get_db_uri(with_driver=True)
        self._engine = engine
    
    def db_read(self):
        """ See: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying
            TODO
            Takes SQL or is designed specifically for a recognized query pattern in the application

            returns result
        """
        pass

    def db_write(self, db_objs: list):
        """
            Attempting cleaner version of _db_write
        """
        with Session.begin() as session:
            try:
                # Add all in bulk TODO explore pros/cons again
                session.add_all(db_objs)
            except Exception as e:
                # TODO Error handling
                session.rollback()
                raise e
            else:
                session.commit() # Not explicitly required; Handled by Context Manager

    def _db_write(self, db_objs: list):
        """
            The only method that should touch session. This a more
            verbose, but clear, version of some examples here:
            https://docs.sqlalchemy.org/en/20/orm/session_basics.html#framing-out-a-begin-commit-rollback-block

            returns result
        """
        try:
            with _Session(self._engine) as session:
                session.begin()
                try:
                    # Add all in bulk TODO explore pros/cons again
                    session.add_all(db_objs)
                except Exception as e:
                    # TODO Handle error
                    session.rollback()
                    raise e
                else:
                    # Commit
                    session.commit() # Not required with session manager
        except Exception as e:
            # TODO Error handling
            raise e

    def select_relay_by_id(self, relay_id: int) -> Relay:
        sql = select(Relay).where(Relay.id == relay_id)
        result = self.session.scalars(sql)
        return result
    
    def select_all_relays(self) -> list[Relay]:
        relays = self.session.query(Relay).all()
        return relays

