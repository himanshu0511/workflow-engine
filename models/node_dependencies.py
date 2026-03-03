from typing import Optional
from sqlmodel import SQLModel, Field
from models.util.ulid_type import ulid_field

class NodeDependencies(SQLModel, table=True):
    __tablename__ = "node_dependencies"

    # 1. Foreign Key to the DAG (Ensures all nodes belong to the same DAG)
    dag_id: str = ulid_field(
        primary_key=True,
        foreign_key="dag.id",
        index=True
    )

    # 2. The Node that is waiting (The "Child")
    node_id: str = ulid_field(
        primary_key=True,
        foreign_key="node.id"
    )

    # 3. The Node it is waiting for (The "Parent")
    depends_on_node_id: str = ulid_field(
        primary_key=True,
        foreign_key="node.id"
    )

    # Helper property for code readability
    @property
    def depends_on(self) -> str:
        return self.depends_on_node_id
