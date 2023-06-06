import uuid
from utils import new_subscription_id
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
def _run_process(
        relay: Relay, 
        msg_pool: MessagePool, 
        io_loop: tornado.ioloop.IOLoop
    ) -> list:
    # Store Events
    events = []
    try:
        io_loop.run_sync(relay.connect)
    except gen.Return:
        # TODO What is going on here?
        pass
    io_loop.stop()
    # Check for EOSE - Just exploring this
    while msg_pool.has_eose_notices():
        eose = msg_pool.get_all_eose()
        print(eose[0])
    # Check for notices
    while msg_pool.has_notices():
        notice = msg_pool.get_notice()
        # TODO Handle notice
        print(f"NOTICE RECEIVED: {notice.content}")
    # Handle Events
    events = msg_pool.get_all_events()
    transformed = handle_text_note_bulk([event.event for event in events])
    # while msg_pool.has_events():
    #     msg = msg_pool.get_event()
    #     events.append(msg)
    #     print(f"EVENT SEEN: {msg.event.content}")
    # post_process_events = msg_pool.get_all_events()
    # Finish
    print(f"Last event: ", events[-1])    

def skeleton_process():
    message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    io_loop = tornado.ioloop.IOLoop.current()
    # Relay
    r = Relay(
        RELAY_URL,
        message_pool,
        io_loop,
        policy,
        timeout=TIMEOUT
    )
    # Filters List    
    filters = FiltersList(
        [
            Filters(
                kinds=[EventKind.TEXT_NOTE],
                limit=3,
            )
        ]
    )
    # Subscription
    subscription_id = new_subscription_id()
    r.add_subscription(subscription_id, filters)
    _run_process(
        relay=r,
        msg_pool=message_pool,
        io_loop=io_loop
    )
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