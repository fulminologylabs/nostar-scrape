from typing import Any, List
from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.types import JSON, DateTime
from utils import default_relay_config_epoch_start
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
    }

# Tables
class Relay(Base):
    __tablename__ = "relay"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url        : Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name       : Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp())
    updated_at : Mapped[datetime] = mapped_column(index=True, server_onupdate=func.current_timestamp())
    # Relationships
    relay_config : Mapped["RelayConfig"] = relationship(back_populates="relay")


class RelayConfig(Base):
    __tablename__ = "relay_config"
    relay_id    : Mapped[int] = mapped_column(ForeignKey("relay.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False,)
    epoch_start : Mapped[datetime] = mapped_column(server_default=default_epoch_relay_config)
    updated_at  : Mapped[datetime] = mapped_column(server_onupdate=(func.current_timestamp()))
    # Relationships
    relay       : Mapped["Relay"] = relationship(back_populates="relay_config")


class Filter(Base):
    __tablename__ = "filter"
    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    json        : Mapped[dict_from_json] = mapped_column(nullable=False)
    name        : Mapped[str] = mapped_column(nullable=True, unique=True)
    created_at  : Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    updated_at  : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp())
    

class EventKind(Base):
    __tablename__ = "event_kind"
    event_id    : Mapped[int] = mapped_column(primary_key=True)
    name        : Mapped[str] = mapped_column(nullable=True, unique=True)
    created_at  : Mapped[datetime] = mapped_column(server_default=func.current_timestamp(), index=True)
    updated_at  : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp())


# TODO should we have `completed` col?
class Batch(Base):
    __tablename__ = "batch"
    batch_id   : Mapped[int] = mapped_column(primary_key=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp())
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp())


class JobType(Base):
    __tablename__ = "job_type"
    id         : Mapped[int] = mapped_column(primary_key=True)
    type       : Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp())
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp())
    # Relationships


class Job(Base):
    __tablename__ = "job"
    id         : Mapped[int] = mapped_column(primary_key=True)
    relay_id   : Mapped[int] = mapped_column(ForeignKey("relay.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    filter_id  : Mapped[int] = mapped_column(ForeignKey("filter.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    batch_id   : Mapped[int] = mapped_column(ForeignKey("batch.batch_id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True)
    job_type   : Mapped[int] = mapped_column(ForeignKey("job_type.id", onupdate="CASCADE", ondelete="CASCADE"), index=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp())
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp())    
    # Relationships
    relay         : Mapped["Relay"] = relationship()
    filter        : Mapped["Filter"] = relationship()
    batch         : Mapped["Batch"] = relationship()
    job_name      : Mapped["JobType"] = relationship()    
    subscriptions : Mapped[List["Subscription"]] = relationship(back_populates="job")

class Subscription(Base):
    __tablename__ = "subscription"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_id     : Mapped[int] = mapped_column(ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    start_time : Mapped[datetime] = mapped_column(nullable=False, index=True)
    end_time   : Mapped[datetime] = mapped_column(nullable=False, index=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp())
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp()) 
    # Relationships
    job        : Mapped["Job"] = relationship(back_populates="subs")


class TextNote(Base):
    __tablename__ = "text_note"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event      : Mapped[int] = mapped_column(ForeignKey("event_kind.event_id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    job_id     : Mapped[int] = mapped_column(ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    data       : Mapped[dict_from_json] = mapped_column(nullable=False)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=func.current_timestamp())
    updated_at : Mapped[datetime] = mapped_column(server_onupdate=func.current_timestamp())     
    # Relationships
    event_kind : Mapped["EventKind"] = relationship()
    job        : Mapped["Job"] = relationship()

