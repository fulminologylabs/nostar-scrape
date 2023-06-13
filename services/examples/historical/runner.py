from utils import new_subscription_id, new_job_id, new_batch_id
from services.db import DBService
import tornado.ioloop
from tornado import gen
from pynostr.relay import Relay
from pynostr.message_pool import MessagePool
from services.mappers.events.text_note import handle_text_note_bulk

def _run(
        relay: Relay,
        db: DBService,
        msg_pool: MessagePool, 
        io_loop: tornado.ioloop.IOLoop,
    ) -> list:
    # New Job ID TODO This might need to move
    JOB_ID = new_job_id()
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