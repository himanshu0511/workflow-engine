import datetime
from enum import Enum
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum as SAEnum, text
from models.util.ulid_type import ulid_field

# values def/condional/exec/network/email/sms/whatsapp
class NodeType(str, Enum):
    DEF = 'def'
    COND = 'cond'
    EXEC = 'exec'
    NETWORK = 'network'
    EMAIL = 'email'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'

class RetryType(str, Enum):
    NONE = 'none'
    FIXED = 'fixed'
    EXPONENTIAL = 'exponential'
    LINEAR = 'linear'



class Node(SQLModel, table=True):
    # 1. Primary Key (Auto-generates ULID)
    id: str = ulid_field(primary_key=True)

    # 2. Foreign Key (Links to DAG table, uses BINARY(16))
    dag_id: str = ulid_field(index=True, foreign_key="dag.id")

    # 3. Native MySQL Enums
    type: NodeType = Field(
        sa_column=Column(SAEnum(NodeType), nullable=False)
    )

    retry_type: RetryType = Field(
        default=RetryType.NONE,
        sa_column=Column(SAEnum(RetryType), nullable=False, server_default=RetryType.NONE)
    )

    # 4. Node Logic
    source: str = Field(max_length=1024)  # Increased length for source code/scripts
    initial_delay: int = Field(default=0)
    max_delay: int = Field(default=0)
    factor: float = Field(default=1.0)
    max_retries: int = Field(default=0)

    # 5. Timestamps
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )

    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        }
    )
