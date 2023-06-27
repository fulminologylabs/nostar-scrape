"""db lookup inserts

Revision ID: e862323037c5
Revises: 02a52963a48c
Create Date: 2023-06-13 07:48:11.671245

"""
import json
from alembic import op
from pynostr.event import EventKind
from app.utils import default_relay_config_epoch_start
from migrations.utils import sql_fetch_all
from app.constants import HISTORICAL_JOBS, DAILY_JOBS
# revision identifiers, used by Alembic.
revision = 'e862323037c5'
down_revision = '02a52963a48c'
branch_labels = None
depends_on = None
# And create for each of the below tables:
# Relay
# RelayConfig
# Filter
# EventKind
# JobType
# Status
STARTER_RELAYS = [
    {
        "name": "Damus",
        "url": "wss://relay.damus.io",
    },
]

STARTER_FILTERS = [
    {
        "name": "underlying_text_note",
        "json": {
            "kinds": [EventKind.TEXT_NOTE],
            "limit": -1,
            "since": -1,
            "until": -1,
        }
    }
]
STARTER_EVENT_KINDS = [EventKind.TEXT_NOTE,]
# JobTypes
H_JOBS = [jtype.value for jtype in HISTORICAL_JOBS]
D_JOBS = [jtype.value for jtype in DAILY_JOBS]
STARTER_JOB_TYPES   = H_JOBS + D_JOBS

STARTER_SUB_STATUS  = [
    ("PENDING", "Job subscriptions created and scheduled."), 
    ("STARTED", "Job subscription is in-progress."), 
    ("FAILED", "Job subscription errored before completion."), 
    ("COMPLETED", "Job finished successfully."),
]

def _get_relay_ids() -> list:
    relay_ids: list = sql_fetch_all("SELECT id FROM relay;")
    return relay_ids

def _get_filter_ids() -> list:
    filter_ids: list = sql_fetch_all("SELECT id FROM filter;")
    return filter_ids

def upgrade() -> None:
    epoch_start = default_relay_config_epoch_start()
    # Relay
    for relay in STARTER_RELAYS:
        op.execute(f"INSERT INTO relay (name, url) VALUES ('{relay['name']}', '{relay['url']}');")
    # RelayConfig
    for id in _get_relay_ids():
        # See here: https://www.commandprompt.com/education/postgresql-to_timestamp-function-with-examples/
        op.execute(
            f"INSERT INTO relay_config (relay_id, epoch_start)\
            VALUES ({id[0]}, TO_TIMESTAMP('%s', 'YYYY-MM-DD HH24:MI:SS'));" % epoch_start
        )
    # Filters
    for filter in STARTER_FILTERS:
        op.execute(f"INSERT INTO filter (json, name) VALUES ('{json.dumps(filter)}', '{filter['name']}')")
    # EventKinds
    for kind in STARTER_EVENT_KINDS:
        name = EventKind(kind).name
        op.execute(f"INSERT INTO event_kind (event_id, name) VALUES ({kind.value}, '{name}');")
    # JobType
    for jtype in STARTER_JOB_TYPES:
        op.execute(f"INSERT INTO job_type (process, filter_id, description) VALUES ('{jtype}', 1, 'handles underlying text note events.');")
    # Status
    for status in STARTER_SUB_STATUS:
        op.execute(f"INSERT INTO status (status, description)\
                   VALUES ('{status[0]}', '{status[1]}');")

def downgrade() -> None:
    # Drop Relay and Relay Config
    for id in _get_relay_ids():
        op.execute(f"DELETE FROM relay_config WHERE relay_id = {id[0]};")
        op.execute(f"DELETE FROM relay WHERE id = {id[0]};")
    # Drop Filter
    for id in _get_filter_ids():
        op.execute(f"DELETE FROM filter WHERE id = {id[0]};")
    # Drop EventKinds
    for kind in STARTER_EVENT_KINDS:
        op.execute(f"DELETE FROM event_kind WHERE event_id = {kind.value};")
    # Drop JobTypes
    bulk_delete_types: str = str(STARTER_JOB_TYPES).replace("[", "").replace("]", "")
    op.execute(
        f"DELETE FROM job_type WHERE type IN ({bulk_delete_types});"
    )
    # Drop Subscription Status
    status_names: list = [status[0] for status in STARTER_SUB_STATUS]
    bulk_delete_status: str = str(status_names).replace("[", "").replace("]", "")
    op.execute(f"DELETE FROM status WHERE status IN ({bulk_delete_status});")
