from app.repository.models import Relay, Base, RelayConfig, Job, \
    JobType, EventKind, Filter, Subscription, Event
from app.repository.connection import engine, Session, yield_db_session
from app.utils import load_environment_variables, get_db_uri
from sqlalchemy.orm import Session as _Session
from sqlalchemy import select

# TODO Eventually the goal is to use this service to standardize:
# DB inserts, updates, deletes, and selects
# sqlalchemy session.add, session.add_all, session.commit, session.refresh,
#            session.refresh_all, session.flush, session.rollback, session.close
#            session.begin_nested, etc.

# For help with developing new queries: https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
# For help with updating / deleting using the DB Models see below for help:
# https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire
class DBService:
    def __init__(self):
        #load_environment_variables()
        #self._db_uri = get_db_uri(with_driver=True)
        self._engine = engine
        self._bulk_limit = 1000

    def read(self, sql: str):
        """ See: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying
            TODO
            Takes SQL or is designed specifically for a recognized query pattern in the application

            returns result
        """
        pass

    def write(self, db_objs: list, batch: bool = False):
        """
            Attempting cleaner version of _db_write

            if large batch leverage flush other
            sqlalchemy tools to prevent lost data
            during a long or large transaction.
        """
        # if len(db_objs) > self._bulk_limit:
        #     # TODO create a bulk condition that indicates
        #     # the need to make explicit session.flush() calls.
        #     # Consider breaking db_objs into sets of at-most 1000 items
        #     # and then calling session.add_all() and session.flush() for every
        #     # list of at-most 1000 items contained in db_objs
        #     batches = [
        #         db_objs[i * self._bulk_limit:(i + 1) * self._bulk_limit] for i \
        #         in range((len(db_objs) + self._bulk_limit - 1) // self._bulk_limit)
        #     ]
        with Session.begin() as session:
            try:
                # Add all in bulk TODO explore pros/cons again
                session.add_all(db_objs)
                # Batch and Single Batch logic
                # for batch in batches:
                #     session.add_all(batch)
                #     session.flush()   
            except Exception as e:
                # TODO Error handling
                session.rollback()
                raise e
            else:
                session.commit() # Not explicitly required; Handled by Context Manager

    def _db_write_bulk(self, db_objs: list):
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

    def _db_write_one(self, db_obj):
        try:
            with _Session(self._engine) as session:
                session.begin()
                try:
                    session.add(db_obj)
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

