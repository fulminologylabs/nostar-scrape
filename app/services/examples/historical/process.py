from app.utils import new_subscription_id, new_job_id
from services.db import DBService
from services.examples.historical.runner import _run
from services.examples.historical.configs import CONFIG
import tornado.ioloop
from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
# TODO Are subscriptions being closed properly?
RELAY_URL = "wss://relay.damus.io"
TIMEOUT = 300
LIMIT = 5
JOB_ID = new_job_id()

def skeleton_process():
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
    # TODO get from DB (Job) Filters List    
    filters = FiltersList(
        [
            Filters(
                kinds=[EventKind.TEXT_NOTE],
                limit=3,
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
        io_loop=io_loop
    )

if __name__ == "__main__":
    skeleton_process()
