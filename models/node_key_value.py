from typing import Optional
from sqlalchemy import Column, String as SAString, Text as SAText
from sqlmodel import SQLModel, Field
from models.util.ulid_type import ulid_field

class NodeKeyValue(SQLModel, table=True):
    __tablename__ = "node_key_value"

    # 1. The Group Identifier (ULID)
    # This links many keys to one execution context or group.
    group_id: str = ulid_field(primary_key=True, index=True)

    # 2. The Key
    # We make this part of the primary key so (group_id, key) is unique.
    key: str = Field(
        sa_column=Column(SAString(255), primary_key=True, nullable=False)
    )

    # 3. The Value
    # Using SAText (MySQL TEXT) instead of String if values might be large (JSON, etc.)
    # If values are always short, you can use SAString(1024)
    value: str = Field(sa_column=Column(SAText, nullable=False))
