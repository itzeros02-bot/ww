"""QueryHistory SQLModel entity."""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Text, DateTime
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class QuerySource(str, Enum):
    """Query source type."""

    MANUAL = "manual"
    NATURAL_LANGUAGE = "natural_language"


class QueryHistory(SQLModel, table=True):
    """Query history entity stored in SQLite."""

    __tablename__ = "queryhistory"

    id: Optional[int] = Field(default=None, primary_key=True)
    database_name: str = Field(foreign_key="databaseconnections.name")
    sql_text: str = Field(sa_column=Column(Text))
    executed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        sa_column=Column(DateTime(timezone=False), index=True),
    )
    execution_time_ms: Optional[int] = None
    row_count: Optional[int] = None
    success: bool
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    query_source: QuerySource = Field(default=QuerySource.MANUAL)
