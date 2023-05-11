from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from constants import RELAY_LIST
import time
import uuid
from datetime import datetime, time, timedelta, timezone

#1_SUB_ID = "e304a8b2eb7d11ed82eaaa665a0df9e3" # 37836
START_A = int(datetime.strptime("01/01/2021", "%d/%m/%Y").strftime("%s"))
START_B = int(datetime.strptime("01/01/2020", "%d/%m/%Y").strftime("%s"))
START_C = int(datetime.strptime("01/01/2020", "%d/%m/%Y").strftime("%s"))
yesterday_midnight = datetime.combine(datetime.today(), time.min, tzinfo=timezone.utc).timestamp()
#1_UNTIL = int(yesterday_midnight)
UNTIL_A = int(datetime.strptime("09/01/2021", "%d/%m/%Y").strftime("%s"))
UNTIL_B = int(datetime.strptime("01/01/2021", "%d/%m/%Y").strftime("%s"))
# TODO revisit the initial NIPS and see how we can evaluate 
# when our subscription has retreived everything the Relay
# has for the filter
def trial():
    relay_manager = RelayManager(timeout=300)
    for relay in RELAY_LIST:
        relay_manager.add_relay(relay)
        #relay_manager.add_relay(relay)

    #filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], since=START, until=UNTIL)])
    filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], since=START_C, until=UNTIL_A)])
    subscription_id = uuid.uuid1().hex
    print("SUB ID: ", subscription_id)
    # Start Connection    
    #relay_manager.add_subscription_on_all_relays(SUB_ID, filters)
    relay_manager.add_subscription_on_all_relays(subscription_id, filters)
    relay_manager.run_sync()
    # Tallys
    events = []
    total_reqs = 0

    # init_start = START
    # current_start = init_start
    # init_end = init_start + 5 * 60 * 60
    # current_end = init_end

    while relay_manager.message_pool.has_notices():
        notice_msg = relay_manager.message_pool.get_notice()
        print("NOTICE _____", notice_msg.content)

    while relay_manager.message_pool.has_events():
        total_reqs += 1
        event_msg = relay_manager.message_pool.get_event()
        print(event_msg.event)
        events.append(event_msg)

    # Close Connection
    print(len(events))
    print(total_reqs)
    #relay_manager.close_subscription_on_all_relays()
    relay_manager.close_all_relay_connections()
