"""db lookup inserts

Revision ID: e862323037c5
Revises: 02a52963a48c
Create Date: 2023-06-13 07:48:11.671245

"""
import json
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.sql import table, column
from pynostr.event import EventKind
from app.utils import default_relay_config_epoch_start
# revision identifiers, used by Alembic.
revision = 'e862323037c5'
down_revision = '02a52963a48c'
branch_labels = None
depends_on = None
# TODO Start here: https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.bulk_insert
# And create for each of the below tables:
# Relay
# RelayConfig
# Filter
# EventKind
# JobType
# SubscriptionStatus
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
STARTER_EVENT_KINDS = [EventKind.TEXT_NOTE]
STARTER_JOB_TYPES   = ["HIST", "DAILY",]
STARTER_SUB_STATUS  = ["pending", "started", "failed", "completed"]


def upgrade() -> None:
    epoch_start = default_relay_config_epoch_start()
    # Relay and RelayConfig
    for idx, relay in enumerate(STARTER_RELAYS):
        op.execute(f"INSERT INTO relay (name, url) VALUES ('{relay['name']}', '{relay['url']}');")
        # See here: https://www.commandprompt.com/education/postgresql-to_timestamp-function-with-examples/
        op.execute(
            f"INSERT INTO relay_config (relay_id, epoch_start)\
            VALUES ({idx+1}, TO_TIMESTAMP('%s', 'YYYY-MM-DD HH24:MI:SS'));" % epoch_start
        )
    # Filters
    for _, filter in enumerate(STARTER_FILTERS):
        op.execute(f"INSERT INTO filter (json, name) VALUES ('{json.dumps(filter)}', '{filter['name']}')")

def downgrade() -> None:
    # Drop Relay and Relay Config
    for idx, _ in enumerate(STARTER_RELAYS):
        op.execute(f"DELETE FROM relay_config WHERE relay_id = {idx+1};")
        op.execute(f"DELETE FROM relay WHERE id = {idx + 1};")
    # Drop Filter
    for idx, _ in enumerate(STARTER_FILTERS):
        op.execute(f"DELETE FROM filter WHERE id = {idx + 1};")
