import datetime
from typing import Optional

from sqlalchemy import Column, Enum as SAEnum, String as SAString, DateTime, text
from sqlmodel import SQLModel, Field

from models.enums.dag_type import DagType
from models.util.ulid_type import ulid_field


class DAG(SQLModel, table=True):
    # 1. Primary Key using your ULID util
    id: str = ulid_field(primary_key=True)

    # 2. Native MySQL Enum - Pydantic handles validation automatically
    type: DagType = Field(
        sa_column=Column(SAEnum(DagType), nullable=False)
    )

    # 3. Strings with explicit lengths for MySQL indexing
    name: str = Field(index=True, unique=True, max_length=255)
    description: str = Field(max_length=255, nullable=False)

    # 4. Automated Timestamps
    # createdAt: Set once on creation
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )

    # updatedAt: Updates every time the row is modified (MySQL native feature)
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        }
    )

    # 5. Optional fields
    cron_string: Optional[str] = Field(default=None, max_length=255)
    next_run: Optional[datetime.datetime] = Field(default=None)
