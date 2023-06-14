"""db lookup inserts

Revision ID: e862323037c5
Revises: 02a52963a48c
Create Date: 2023-06-13 07:48:11.671245

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'e862323037c5'
down_revision = '02a52963a48c'
branch_labels = None
depends_on = None
# TODO Start here: https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.bulk_insert
# And create for each of the below tables:
# Relay
# Filter
# EventKind
# JobType
# BatchStatus
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
            # TODO Left Off here - create mock filter JSON
            # TODO Will filters work with None values or will that carry some meaning
        }
    }
]
STARTER_EVENT_KINDS = []
STARTER_JOB_TYPES = []
STARTER_BATCH_STATUSES = []

def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
