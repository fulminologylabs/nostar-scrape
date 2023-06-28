from __future__ import annotations
from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, text, JSON
from sqlalchemy.types import JSON, DateTime
from app.utils import default_relay_config_epoch_start
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# Epoch start
default_epoch_relay_config = default_relay_config_epoch_start()

class Base(DeclarativeBase):
    """
        DB Base Class
    """
    type_annotation_map = {
        dict: JSON, # TODO explore MutableDict use
        datetime: DateTime,
    }

# Tables
class Relay(Base):
    __tablename__ = "relay"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url        : Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name       : Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=text("statement_timestamp()"))
    updated_at : Mapped[datetime] = mapped_column(index=True, onupdate=text("statement_timestamp()"))
    # Relationships: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
    relay_config : Mapped[RelayConfig | None] = relationship(back_populates="relay")


class RelayConfig(Base):
    __tablename__ = "relay_config"
    relay_id    : Mapped[int] = mapped_column(ForeignKey("relay.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False,)
    epoch_start : Mapped[datetime] = mapped_column(default=default_epoch_relay_config)
    updated_at  : Mapped[datetime] = mapped_column(onupdate=text("statement_timestamp()"))
    # Relationships: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
    relay       : Mapped[Relay] = relationship(back_populates="relay_config")


class Filter(Base):
    """
    Think of filter json as a template.

    `limit` `since` and `until` parameters need to be rotated
    many times for each job.
    """
    __tablename__ = "filter"
    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    json        : Mapped[dict] = mapped_column(nullable=False)
    name        : Mapped[str | None] = mapped_column(nullable=True, unique=True)
    created_at  : Mapped[datetime] = mapped_column(server_default=text("statement_timestamp()"))
    updated_at  : Mapped[datetime] = mapped_column(onupdate=text("statement_timestamp()"))
    

class EventKind(Base):
    __tablename__ = "event_kind"
    event_id    : Mapped[int] = mapped_column(primary_key=True) # Match: https://github.com/nostr-protocol/nips#event-kinds
    name        : Mapped[str | None] = mapped_column(nullable=True, unique=True)
    created_at  : Mapped[datetime] = mapped_column(server_default=text("statement_timestamp()"), index=True)
    updated_at  : Mapped[datetime] = mapped_column(onupdate=text("statement_timestamp()"))


class Status(Base):
    __tablename__ = "status"
    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status      : Mapped[str] = mapped_column(nullable=False)
    description : Mapped[str] = mapped_column(nullable=True)


class JobType(Base):
    __tablename__ = "job_type"
    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    process    : Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    filter_id  : Mapped[int] = mapped_column(ForeignKey("filter.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=text("statement_timestamp()"))
    updated_at : Mapped[datetime] = mapped_column(onupdate=text("statement_timestamp()"))
    # Relationships: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
    filter: Mapped[Filter] = relationship()


class Job(Base):
    """
        Consider this approach to the Job table in the future (if it fits):
        https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many
    """
    __tablename__ = "job"
    id         : Mapped[str] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    relay_id   : Mapped[int] = mapped_column(ForeignKey("relay_config.relay_id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    job_type   : Mapped[int] = mapped_column(ForeignKey("job_type.id", onupdate="CASCADE", ondelete="CASCADE"), index=True)
    status_id  : Mapped[int] = mapped_column(ForeignKey("status.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    start_time : Mapped[datetime] = mapped_column(nullable=False, index=True)
    created_at : Mapped[datetime] = mapped_column(index=True, server_default=text("statement_timestamp()"))
    updated_at : Mapped[datetime] = mapped_column(onupdate=text("statement_timestamp()"))    
    # Relationships: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
    status        : Mapped[Status] = relationship()
    relay_config  : Mapped[RelayConfig] = relationship(lazy="select")
    job_desc      : Mapped[JobType] = relationship(lazy="select")    
    subscriptions : Mapped[List[Subscription]] = relationship(back_populates="job")


class Subscription(Base):
    # TODO Do we need tags
    __tablename__ = "subscription"
    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_id      : Mapped[int] = mapped_column(ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    ended_at    : Mapped[int] = mapped_column(nullable=False, index=True)
    started_at  : Mapped[int] = mapped_column(nullable=True, index=True)
    status_id   : Mapped[int] = mapped_column(ForeignKey("status.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    created_at  : Mapped[datetime] = mapped_column(index=True, server_default=text("statement_timestamp()"))
    filter_json : Mapped[dict] = mapped_column(nullable=True)
    updated_at  : Mapped[datetime] = mapped_column(onupdate=text("statement_timestamp()")) 
    # Relationships: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
    job                 : Mapped[Job | None] = relationship(back_populates="subscriptions")
    status              : Mapped[Status | None] = relationship()

class Event(Base):
    __tablename__ = "event"
    id            : Mapped[int] = mapped_column(primary_key=True)
    event_kind_id : Mapped[int] = mapped_column(ForeignKey("event_kind.event_id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    job_id        : Mapped[int] = mapped_column(ForeignKey("job.id", onupdate="CASCADE", ondelete="RESTRICT"), index=True)
    content       : Mapped[str] = mapped_column(nullable=False)
    tags          : Mapped[dict | None] = mapped_column(nullable=True)
    pubkey        : Mapped[str] = mapped_column(nullable=False)
    created_at    : Mapped[int] = mapped_column(nullable=False)
    signature     : Mapped[str] = mapped_column(nullable=False)
    inserted_at   : Mapped[datetime] = mapped_column(index=True, server_default=text("statement_timestamp()"))
    updated_at    : Mapped[datetime] = mapped_column(onupdate=text("statement_timestamp()"))     
    # Relationships: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
    event_kind: Mapped[EventKind] = relationship()
    job        : Mapped[Job] = relationship()

