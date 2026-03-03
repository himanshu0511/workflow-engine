import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Enum as SAEnum, text, Index
from sqlmodel import SQLModel, Field

# Assuming this is your custom utility
from models.util.ulid_type import ulid_field


class DagStatus(str, Enum):
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    TO_BE_EXECUTED = 'to_be_executed'


class DagAudit(SQLModel, table=True):
    # 1. The unique record ID for this audit entry
    id: str = ulid_field(primary_key=True)

    # 2. Relational IDs (All mapped to BINARY(16) in MySQL via ulid_field)
    # Note: primary_key=False ensures these don't auto-generate new ULIDs
    dag_id: str = ulid_field(index=True, foreign_key="dag.id")
    node_id: str = ulid_field(index=True)
    dag_instance_id: str = ulid_field(index=True)
    node_instance_id: str = ulid_field(index=True)

    # Use Optional for IDs that might not exist yet
    input_key_value_group_id: Optional[str] = ulid_field(default=None, nullable=True)

    # 3. Status & Logic
    status: DagStatus = Field(
        sa_column=Column(SAEnum(DagStatus), nullable=False, server_default=DagStatus.TO_BE_EXECUTED)
    )
    retry_count: int = Field(default=0)

    # 4. Timestamps
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    next_retry_time: Optional[datetime.datetime] = Field(default=None)
    execution_end_time: Optional[datetime.datetime] = Field(default=None)

    # 5. Composite Index for common "Filter by instance status" queries
    __table_args__ = (
        Index("ix_dag_inst_status", "dag_instance_id", "status"),
    )
