import uuid
from typing import Any, List
from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.types import JSON, DateTime
from utils import default_relay_config_epoch_start
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# Epoch start
default_epoch_relay_config = default_relay_config_epoch_start()
# Type Alias for Mapping Postgres JSON to Python Dict
dict_from_json = dict[str, Any]

class Base(DeclarativeBase):
    """
        DB Base Class
    """
    type_annotations_map = {
        dict_from_json: JSON,
        datetime: DateTime,
        int: UUID,
    }

# Tables
class Relay(Base):
    __tablename__ = "relay"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url        : Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name       : Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp)
    updated_at : Mapped[datetime] = mapped_column(index=True, server_onupdate=func.current_timestamp)
    # Relationships
    relay_config : Mapped["RelayConfig" | None] = relationship(back_populates="relay")


class RelayConfig(Base):
    __tablename__ = "relay_config"
    relay_id    : Mapped[int] = mapped_column(ForeignKey("relay.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False,)
    epoch_start : Mapped[datetime] = mapped_column(server_default=default_epoch_relay_config)
    updated_at  : Mapped[datetime] = mapped_column(server_onupdate=(func.current_timestamp))
    # Relationships
    relay       : Mapped["Relay"] = relationship(back_populates="relay_config")


class Filter(Base):
    __tablename__ = "filter"
    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    json        : Mapped[dict_from_json] = mapped_column(nullable=False)
    name        : Mapped[str | None] = mapped_column(nullable=True, unique=True)
    created_at  : Mapped[datetime] = mapped_column(server_default=func.current_timestamp)
    updated_at  : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp)
    

class EventKind(Base):
    __tablename__ = "event_kind"
    event_id    : Mapped[int] = mapped_column(primary_key=True) # Match: https://github.com/nostr-protocol/nips#event-kinds
    name        : Mapped[str | None] = mapped_column(nullable=True, unique=True)
    created_at  : Mapped[datetime] = mapped_column(server_default=func.current_timestamp, index=True)
    updated_at  : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp)


# TODO should we have `completed` col?
class Batch(Base):
    __tablename__ = "batch"
    batch_id     : Mapped[int]      = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id       : Mapped[int]      = mapped_column(ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    starts_at    : Mapped[datetime] = mapped_column(index=True, nullable=False)
    completed_at : Mapped[datetime] = mapped_column(index=True, nullable=True)
    status_id    : Mapped[int]      = mapped_column(ForeignKey("batch_status.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    created_at   : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp)
    updated_at   : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp)
    # Relationships
    status : Mapped["BatchStatus"] = relationship()
    job    : Mapped["Job"] = relationship(back_populates="batch")


class BatchStatus(Base):
    __tablename__ = "batch_status"
    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status      : Mapped[str] = mapped_column(nullable=False)
    description : Mapped[str] = mapped_column(nullable=True)


class JobType(Base):
    __tablename__ = "job_type"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type       : Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp)
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp)
    # Relationships


class Job(Base):
    """
        Consider this approach to the Job table in the future (if it fits):
        https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many
    """
    __tablename__ = "job"
    id         : Mapped[int] = mapped_column(primary_key=True, default=uuid.uuid4)
    relay_id   : Mapped[int] = mapped_column(ForeignKey("relay.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    filter_id  : Mapped[int] = mapped_column(ForeignKey("filter.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    job_type   : Mapped[int] = mapped_column(ForeignKey("job_type.id", onupdate="CASCADE", ondelete="CASCADE"), index=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp)
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp)    
    # Relationships
    relay         : Mapped["Relay"] = relationship()
    filter        : Mapped["Filter"] = relationship()
    batch         : Mapped[List["Batch"]] = relationship(back_populates="job")
    job_name      : Mapped["JobType"] = relationship()    
    subscriptions : Mapped[List["Subscription"]] = relationship(back_populates="job")


class Subscription(Base):
    # TODO Do we need tags
    __tablename__ = "subscription"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_id     : Mapped[int] = mapped_column(ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    start_time : Mapped[datetime] = mapped_column(nullable=False, index=True)
    end_time   : Mapped[datetime] = mapped_column(nullable=False, index=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp)
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp) 
    # Relationships
    job        : Mapped["Job" | None] = relationship(back_populates="subs")


class Event(Base):
    __tablename__ = "event"
    id            : Mapped[int] = mapped_column(primary_key=True)
    event_kind_id : Mapped[int] = mapped_column(ForeignKey("event_kind.event_id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    job_id        : Mapped[int] = mapped_column(ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    content       : Mapped[str] = mapped_column(nullable=False)
    tags          : Mapped[dict_from_json | None] = mapped_column(nullable=True)
    pubkey        : Mapped[str] = mapped_column(nullable=False)
    created_at    : Mapped[int] = mapped_column(nullable=False)
    signature     : Mapped[str] = mapped_column(nullable=False)
    inserted_at   : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp)
    updated_at    : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp)     
    # Relationships
    event_kind: Mapped["EventKind"] = relationship()
    job        : Mapped["Job"] = relationship()

