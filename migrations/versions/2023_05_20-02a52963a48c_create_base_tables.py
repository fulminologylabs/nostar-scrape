"""create_base_tables

Revision ID: 02a52963a48c
Revises: 
Create Date: 2023-05-20 18:03:57.640076

"""
from alembic import op
import sqlalchemy as sa
from app.utils import default_relay_config_epoch_start
# revision identifiers, used by Alembic.
revision = '02a52963a48c'
down_revision = None
branch_labels = None
depends_on = None

default_epoch_start = default_relay_config_epoch_start()
def upgrade() -> None:
    # Relay
    op.create_table(
        'relay',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(256), nullable=True, unique=True),
        sa.Column('url', sa.String(1200), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("statement_timestamp()"), index=True),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"), index=True)
    )
    # Relay Config
    op.create_table(
        'relay_config',
        sa.Column('relay_id', sa.Integer, sa.ForeignKey('relay.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, autoincrement='ignore_fk'),
        # TODO Be careful with this default - may need to change to server_default w/ scalar somehow
        sa.Column('epoch_start', sa.DateTime, default=default_epoch_start),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"))
    )
    # Filter
    op.create_table(
        'filter',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(256), nullable=True, unique=True),
        sa.Column('json', sa.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("statement_timestamp()")),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"))
    )
    # Event Kind
    op.create_table(
        'event_kind',
        sa.Column('event_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(256), nullable=True, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("statement_timestamp()"), index=True),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"))
    )
    # Job Type
    op.create_table(
        'job_type',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('process', sa.String(256), nullable=False, unique=True),
        sa.Column('description', sa.String(256), nullable=True, unique=False),
        sa.Column('filter_id',sa.Integer, sa.ForeignKey('filter.id', onupdate='CASCADE', ondelete='RESTRICT'), index=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("statement_timestamp()"), index=True),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"))
    )
    # Status
    op.create_table(
        'status',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('status', sa.String(256), nullable=False),
        sa.Column('description', sa.String(1028), nullable=True),
    )
    # Job
    op.create_table('job',
        sa.Column('id', sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('relay_id', sa.Integer, sa.ForeignKey('relay_config.relay_id', onupdate='CASCADE', ondelete='RESTRICT'), index=True),
        sa.Column('job_type', sa.Integer, sa.ForeignKey('job_type.id', onupdate='CASCADE', ondelete='CASCADE'), index=True),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('status.id', onupdate="CASCADE", ondelete="RESTRICT"), index=True),
        sa.Column('start_time', sa.DateTime, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("statement_timestamp()"), index=True),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"))
    )
    # Subscription
    op.create_table('subscription',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('job_id', sa.UUID, sa.ForeignKey('job.id', onupdate='CASCADE', ondelete='RESTRICT'), index=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("statement_timestamp()"), index=True),
        sa.Column('ended_at', sa.Integer, nullable=False, index=True),
        sa.Column('started_at', sa.Integer, nullable=True, index=True),
        sa.Column('filter_json', sa.JSON, nullable=True),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('status.id', onupdate="CASCADE", ondelete="RESTRICT"), index=True),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"))
    )
    # Event
    op.create_table('event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pubkey', sa.String(256), nullable=False),
        sa.Column('created_at', sa.Integer, nullable=False),
        sa.Column('event_kind_id', sa.Integer, sa.ForeignKey('event_kind.event_id', onupdate='CASCADE', ondelete='RESTRICT'), index=True),
        sa.Column('tags', sa.JSON, nullable=True),
        # TODO use a more appropriate type
        sa.Column('content', sa.String(10485760), nullable=False),
        sa.Column('signature', sa.String(256), nullable=False),
        sa.Column('job_id', sa.UUID, sa.ForeignKey('job.id', onupdate='CASCADE', ondelete='RESTRICT'), index=True),
        sa.Column('inserted_at', sa.DateTime, server_default=sa.text("statement_timestamp()"), index=True),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.text("statement_timestamp()"))
    )
def downgrade() -> None:
    op.drop_table('event')
    op.drop_table('subscription')
    op.drop_table('job')
    op.drop_table('status')
    op.drop_table('job_type')
    op.drop_table('event_kind')
    op.drop_table('filter')
    op.drop_table('relay_config')
    op.drop_table('relay')

