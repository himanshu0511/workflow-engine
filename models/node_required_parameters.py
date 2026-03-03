from sqlalchemy import Column, String as SAString
from sqlmodel import SQLModel, Field
from models.util.ulid_type import ulid_field

class NodeRequiredParameters(SQLModel, table=True):
    __tablename__ = "node_required_parameters"

    # 1. Foreign Key to the Node (ULID)
    # Marks this as part of the primary key to cluster parameters by node
    node_id: str = ulid_field(
        primary_key=True,
        foreign_key="node.id",
        index=True
    )

    # 2. The Parameter Key Name
    # Also part of the primary key to ensure (node_id, key) is unique
    key: str = Field(
        sa_column=Column(SAString(255), primary_key=True, nullable=False)
    )

    # 3. Optional: Metadata for the parameter
    # Helpful for UI or validation (e.g., "timeout", "api_key")
    description: str | None = Field(default=None, max_length=255)
