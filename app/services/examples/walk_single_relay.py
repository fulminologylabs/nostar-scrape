from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
import tornado.ioloop
from tornado import gen
#import time
#import ssl
import uuid
from datetime import datetime, timezone, time

START_DATE = "05/12/2023"
END_DATE = "05/13/2023"

YESTERDAY = int(
    datetime.combine(
        datetime.today(), time.min, tzinfo=timezone.utc
    )
    .timestamp()
)
SINCE = int(datetime.strptime(START_DATE, "%m/%d/%Y").strftime("%s")) 
UNTIL = int(datetime.strptime(END_DATE, "%m/%d/%Y").strftime("%s"))

RELAY_URL = "wss://relay.damus.io"
TIMEOUT = 1
LIMIT = 4500

def start():
    #ssl._create_default_https_context = ssl._create_unverified_context
    message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    io_loop = tornado.ioloop.IOLoop.current()
    # Relay
    r = Relay(
        "wss://relay.damus.io",
        message_pool,
        io_loop,
        policy,
        timeout=2
    )
    # Filter List
    filters = FiltersList(
        [
            # Example Filter
            Filters(
                kinds=[EventKind.TEXT_NOTE],
                limit=3,
                since=SINCE,
                until=UNTIL,
            )
        ]
    )
    # Sub ID - NOTE need to track this to close or update
    subscription_id = uuid.uuid1().hex
    r.add_subscription(subscription_id, filters)
    if r.check_nip(45):
        r.add_nip45_count(subscription_id)
    
    try:
        io_loop.run_sync(r.connect)
    except gen.Return:
        pass
    io_loop.stop()
    # Trackers
    events = []
    events_seen = 0
    # @END Trackers
    while message_pool.has_notices():
        notice_msg = message_pool.get_notice()
        print(notice_msg.content)
    while message_pool.has_events():
        event_msg = message_pool.get_event()
        events_seen += 1
        events.append(event_msg.event)
        print(event_msg.event.content)
    while message_pool.has_counts():
        print(f"WE RECEIVED A COUNT RELAY MESSAGE: {message_pool.get_count()}")

    print(f"TOTAL EVENTS SEEN: {events_seen}")
    print(f"First Event seen: {events[0].created_at}")
    print(f"Last Event seen: {events[-1].created_at}")
    print(f"Last event: ", events[-1])