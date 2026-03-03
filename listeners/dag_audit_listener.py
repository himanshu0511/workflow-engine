from sqlalchemy import event, update, inspect
from models.dag_audit import DagAudit, DagStatus

SHARD_COUNT = 20


@event.listens_for(DagAudit, "after_insert")
def increment_shard_on_insert(mapper, connection, target):
    """Write: Randomly pick 1 of 20 rows to avoid lock contention."""
    if target.status == DagStatus.TO_BE_EXECUTED:
        shard_id = random.randint(1, SHARD_COUNT)
        connection.execute(
            update(TaskQueueMetrics)
            .where(TaskQueueMetrics.id == shard_id)
            .values(pending_count=TaskQueueMetrics.pending_count + 1)
        )


@event.listens_for(DagAudit, "after_update")
def track_shard_transitions(mapper, connection, target):
    """Handles status changes (Pending -> Running -> Success)."""
    state = inspect(target)
    history = state.get_history("status", True)

    if not history.has_changes():
        return

    old_status = history.deleted[0] if history.deleted else None
    new_status = target.status
    shard_id = random.randint(1, SHARD_COUNT)

    # 1. Decrement Pending if task is picked up or cancelled
    if old_status == DagStatus.TO_BE_EXECUTED:
        connection.execute(
            update(TaskQueueMetrics).where(TaskQueueMetrics.id == shard_id)
            .values(pending_count=TaskQueueMetrics.pending_count - 1)
        )

    # 2. Manage Busy Slots
    if new_status == DagStatus.RUNNING:
        connection.execute(
            update(TaskQueueMetrics).where(TaskQueueMetrics.id == shard_id)
            .values(busy_slots=TaskQueueMetrics.busy_slots + 1)
        )
    elif old_status == DagStatus.RUNNING:
        connection.execute(
            update(TaskQueueMetrics).where(TaskQueueMetrics.id == shard_id)
            .values(busy_slots=TaskQueueMetrics.busy_slots - 1)
        )
