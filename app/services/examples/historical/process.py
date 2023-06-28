from app.utils import new_subscription_id, new_job_id, \
    get_yesterday_raw, get_first_second_of_date, \
    convert_datetime_to_unix_ts, \
    increment_ts_n_seconds
from app.services.db import DBService
from app.services.examples.historical.runner import _run
import tornado.ioloop
from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
from datetime import timedelta
# TODO Are subscriptions being closed properly?
RELAY_URL = "wss://nostr-pub.wellorder.net"
TIMEOUT = 30
LIMIT = 5
JOB_ID = new_job_id()

def skeleton_process():
    # TODO Write to DB as final step
    db = DBService()
    # TODO Create Time-Based Batches
    # TODO Read Job, Relay, RelayConfig, Filter, Subscription Data from DB
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
    # Start Time from Job
    start_time = get_first_second_of_date(
        get_yesterday_raw() - timedelta(weeks=56)
    )
    # Since Param of Filter
    print(f"STARTING POINT: {start_time}")
    since_param = convert_datetime_to_unix_ts(start_time)
    # Until Param of Filter
    net = 60 * 60  # 1 hour
    until_time = get_first_second_of_date(
        get_yesterday_raw() - timedelta(days=3)
    )
    #until_param = increment_ts_n_seconds(since_param, seconds=net)
    until_param = convert_datetime_to_unix_ts(until_time)
    # Limit Param of Filter
    print(f"{since_param} and {until_param}")
    limit = 500
    # TODO get from DB (Job) Filters List    
    filters = FiltersList(
        [
            Filters(
                kinds=[EventKind.TEXT_NOTE],
                limit=limit,
                #since=since_param,
                # NOTE this with no since param
                # works
                until=since_param,
            )
        ]
    )
    # TODO create from DB Subscription
    subscription_id = new_subscription_id()
    r.add_subscription(subscription_id, filters)
    _run(
        relay=r,
        db=db,
        msg_pool=message_pool,
        io_loop=io_loop,
        limit=limit,
    )

if __name__ == "__main__":
    skeleton_process()
