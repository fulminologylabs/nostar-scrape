import uuid
from utils import new_subscription_id, new_job_id, new_batch_id
from services.db import DBService
from services.mappers.events.text_note import handle_text_note_bulk
import tornado.ioloop
from tornado import gen
from typing import Optional
from datetime import datetime
from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool

# TODO Are subscriptions being closed properly?
RELAY_URL = "wss://relay.damus.io"
TIMEOUT = 300
LIMIT = 5000
JOB_ID = new_job_id()

def _run(
        relay: Relay,
        db: DBService,
        msg_pool: MessagePool, 
        io_loop: tornado.ioloop.IOLoop,
    ) -> list:
    try:
        io_loop.run_sync(relay.connect)
    except gen.Return:
        # TODO What is going on here?
        pass
    io_loop.stop()

    # Check for EOSE - Just exploring this
    while msg_pool.has_eose_notices():
        # TODO Handle EOSE
        eose = msg_pool.get_all_eose()
        print(eose[0])
    # Check for notices
    while msg_pool.has_notices():
        notice = msg_pool.get_notice()
        # TODO Handle notice
        print(f"NOTICE RECEIVED: {notice.content}")
    # Handle Events
    events = msg_pool.get_all_events()
    transformed = handle_text_note_bulk([event.event for event in events], JOB_ID)
    # Finish
    db.write(transformed)    



# Utils - Scratch for now
def _create_filters_list(
        ids: Optional[list] = [],
        pubkeys: Optional[list] = [],
        kinds: Optional[list] = [],
        limit: Optional[list] = [],
        since: Optional[list] = [],
        until: Optional[list] = []
) -> FiltersList:
    """
        Each list assigned to a param must have the same len

        Individual filters are created via index position
    """
    zipped = zip(kinds, limit, since, until)

def _create_filter_from_filters_list_zip(zipped_filters: list) -> FiltersList:
    return []

def _create_filter(id: int, kind: int, limit: int, since: int, until: int) -> Filters:
    """
        Convert params to Filters object
    """
    pass