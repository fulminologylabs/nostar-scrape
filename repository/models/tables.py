from sqlalchemy import Table, MetaData, \
    Column, \
    ForeignKey, \
    JSON, \
    func, \
    Integer, \
    String, \
    DateTime
# SQLAlchemy MetaData 
metadata = MetaData()
"""
    `relay` table
"""
relay = Table(
    "relay",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("url", String(1200), unique=True, index=True, nullable=False),
    Column("name", String(256), unique=True, index=True, nullable=True),
    Column("created_at", DateTime, index=True, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, index=True, server_onupdate=func.current_timestamp())
)
"""
    `relay_config` table
"""
relay_config = Table(
    "relay_config",
    metadata,
    Column(
        "relay_id", 
        Integer,ForeignKey(column="relay.id", onupdate="CASCADE", ondelete="CASCADE"), 
        primary_key=True, 
        nullable=False
    ),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp())
)
"""
    `filter` table
"""
filter = Table(
    "filter",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("json", JSON, nullable=False),
    Column("name", String(256), nullable=True, unique=True),
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp())
)
"""
    `event_kind` table
"""
event_kind = Table(
    "event_kind",
    metadata,
    Column("event_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(256), nullable=True, unique=True),
    Column("created_at", DateTime, server_default=func.current_timestamp(), index=True),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp())
)
"""
    `batch` table
"""
batch = Table(
    "batch",
    metadata,
    Column("batch_id", Integer, primary_key=True),
    Column("created_at", DateTime, server_default=func.current_timestamp(), index=True),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp(), index=True)
)
"""
    `job_type` table
"""
job_type = Table(
    "job_type",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String(256), nullable=False, unique=True),
    Column("created_at", DateTime, server_default=func.current_timestamp(), index=True),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp())
)
"""
    `job` table
"""
job = Table(
    "job",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("relay_id", Integer, ForeignKey("relay.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True),
    Column("filter_id",Integer, ForeignKey("filter.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True),
    Column("batch_id", Integer, ForeignKey("batch.batch_id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True),
    Column("job_type", Integer, ForeignKey("job_type.id", onupdate="CASCADE", ondelete="CASCADE"), index=True),
    Column("created_at", DateTime, server_default=func.current_timestamp(), index=True),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp())
)
"""
    `subscription` table
"""
subscription = Table(
    "subscription",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("job_id", Integer, ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True),
    Column("start_time", DateTime, nullable=False, index=True),
    Column("end_time", DateTime, nullable=False, index=True),   
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp())
)
"""
Scraping results phase 1:

    `text_note` table
"""
text_note = Table(
    "text_note",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event", Integer, ForeignKey("event_kind.event_id", onupdate="CASCADE", ondelete="RESTRICT"), index=True),
    Column("job_id", Integer, ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True),
    Column("data", JSON, nullable=False),
    Column("created_at", DateTime, server_default=func.current_timestamp(), index=True),
    Column("updated_at", DateTime, server_onupdate=func.current_timestamp())
)
