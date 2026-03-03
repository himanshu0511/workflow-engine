import random
from sqlmodel import SQLModel, Field, Session, select, func

class TaskQueueMetrics(SQLModel, table=True):
    __tablename__ = "task_queue_metrics"
    # id 1 through 20
    id: int = Field(primary_key=True)
    pending_count: int = Field(default=0)
    busy_slots: int = Field(default=0)

def get_total_lag(session: Session) -> int:
    """Read: O(1) performance, summing 20 rows is instant in MySQL."""
    statement = select(func.sum(TaskQueueMetrics.pending_count))
    return session.exec(statement).first() or 0
