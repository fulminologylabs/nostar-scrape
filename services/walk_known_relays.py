from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from constants import RELAY_LIST
import time
import uuid

# TODO revisit the initial NIPS and see how we can evaluate 
# when our subscription has retreived everything the Relay
# has for the filter
def trial():
    relay_manager = RelayManager(timeout=2)
    for relay in RELAY_LIST:
        relay_manager.add_relay(relay)
        relay_manager.add_relay(relay)

    filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE])])
    subscription_id = uuid.uuid1().hex
    # Start Connection    
    relay_manager.add_subscription_on_all_relays(subscription_id, filters)
    relay_manager.run_sync()
    while relay_manager.message_pool.has_notices():
        notice_msg = relay_manager.message_pool.get_notice()
        print(notice_msg.content)
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        print(event_msg.event)
    # Close Connection
    relay_manager.close_all_relay_connections()
