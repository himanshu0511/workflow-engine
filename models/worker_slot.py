import datetime
from typing import Optional
from sqlalchemy import Column, text, Enum as SaEnum
from sqlmodel import SQLModel, Field

from models.enums import ExecutionType
from models.util.ulid_type import ulid_field


class WorkerSlot(SQLModel, table=True):
    __tablename__ = "worker_slot"

    # 1. Unique Slot ID (ULID)
    id: str = ulid_field(primary_key=True)

    execution_type: ExecutionType = Field(sa_column=Column(SaEnum(ExecutionType), nullable=False))

    # 2. Lease Information
    # Which physical process/pod currently owns this slot
    owner_id: str = Field(index=True, max_length=255)

    # 3. Status & Lifecycle
    is_busy: bool = Field(default=False, index=True)

    # When this slot's lease expires if not renewed (Heartbeat)
    expires_at: datetime.datetime = Field(
        index=True,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )

    # 4. Optional: Current Task Tracking
    current_dag_instance_id: Optional[str] = ulid_field(
        index=True,
        nullable=True,
        default=None
    )
    # 4. Optional: Current Task Tracking
    current_node_instance_id: Optional[str] = ulid_field(
        index=True,
        nullable=True,
        default=None
    )