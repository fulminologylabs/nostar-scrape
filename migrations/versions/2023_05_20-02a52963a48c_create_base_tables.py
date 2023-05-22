"""create_base_tables

Revision ID: 02a52963a48c
Revises: 
Create Date: 2023-05-20 18:03:57.640076

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '02a52963a48c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Relay
    op.create_table(
        'relay',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(256), nullable=True, unique=True),
        sa.Column('url', sa.String(1200), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.current_timestamp())
    )
    # Relay Config
    op.create_table(
        'relay_config',
        sa.Column('relay_id', sa.Integer, sa.ForeignKey('relay.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, autoincrement='ignore_fk')
    )
    # Filter
    op.create_table(
        'filter',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(256), nullable=True, unique=True),
        sa.Column('json', sa.JSON)
    )
    # Event Kind
    op.create_table(
        'event_kind',
        sa.Column('event_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(256), nullable=True, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp())
    )
    # Batch
    op.create_table(
        'batch',
        sa.Column('batch_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('completed_at', sa.DateTime, nullable=True)
    )
    # Job Type
    op.create_table(
        'job_type',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('type', sa.String(256), nullable=False, unique=True),
    )
    # Job
    op.create_table('job',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('relay_id', sa.Integer, sa.ForeignKey('relay.id', onupdate='CASCADE', ondelete='RESTRICT'),),
        sa.Column('filter_id',sa.Integer, sa.ForeignKey('filter.id', onupdate='CASCADE', ondelete='RESTRICT')),
        sa.Column('batch_id', sa.Integer, sa.ForeignKey('batch.batch_id', onupdate='RESTRICT', ondelete='RESTRICT')),
        sa.Column('job_type', sa.Integer, sa.ForeignKey('job_type.id', onupdate='CASCADE', ondelete='CASCADE')),
    )
    # Subscription
    op.create_table('subscription',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('job_id', sa.Integer, sa.ForeignKey('job.id', onupdate='CASCADE', ondelete='RESTRICT')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('start_time', sa.DateTime, nullable=False),
        sa.Column('end_time', sa.DateTime, nullable=False),
    )
    # Text Note
    op.create_table('text_note',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('event', sa.Integer, sa.ForeignKey('event_kind.event_id', onupdate='CASCADE', ondelete='RESTRICT')),
        sa.Column('data', sa.JSON, nullable=False),
        sa.Column('job_id', sa.Integer, sa.ForeignKey('job.id', onupdate='CASCADE', ondelete='RESTRICT'))
    )
def downgrade() -> None:
    op.drop_table('text_note')
    op.drop_table('subscription')
    op.drop_table('job')
    op.drop_table('job_type')
    op.drop_table('batch')
    op.drop_table('event_kind')
    op.drop_table('filter')
    op.drop_table('relay_config')
    op.drop_table('relay')

