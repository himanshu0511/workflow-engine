from sqlmodel import SQLModel
from models.util.ulid_type import ulid_field


class NodeKeyValueGroup(SQLModel, table=True):
    __tablename__ = "node_key_value_group"

    # 1. The unique Group Identifier (ULID)
    # This acts as the Primary Key for the group.
    group_id: str = ulid_field(primary_key=True)

    # 2. (Optional) Metadata
    # Often helpful to know which DAG or Instance created this group
    # dag_instance_id: Optional[str] = ulid_field(index=True, nullable=True)
