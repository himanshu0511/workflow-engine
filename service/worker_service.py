import datetime
from typing import Optional
from sqlmodel import Session, select
from models.worker_slot import WorkerSlot


class WorkerSlotService:
    @staticmethod
    def acquire_slot(session: Session, worker_id: str, dag_inst_id: str) -> Optional[WorkerSlot]:
        """
        Attempts to lease an available slot using SKIP LOCKED.
        """
        # 1. Atomic select for an idle slot
        stmt = (
            select(WorkerSlot)
            .where(WorkerSlot.is_busy == False)
            .where(WorkerSlot.expires_at > datetime.datetime.utcnow())
            .limit(1)
            .with_for_update(skip_locked=True)
        )

        slot = session.exec(stmt).first()
        if not slot:
            return None

        # 2. Update the lease details
        slot.is_busy = True
        slot.owner_id = worker_id
        slot.current_dag_instance_id = dag_inst_id
        # Lease for 5 minutes
        slot.expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        session.add(slot)
        session.commit()
        session.refresh(slot)
        return slot

    @staticmethod
    def release_slot(session: Session, slot_id: str):
        """Standard release once work is finished."""
        slot = session.get(WorkerSlot, slot_id)
        if slot:
            slot.is_busy = False
            slot.current_dag_instance_id = None
            session.add(slot)
            session.commit()

    @staticmethod
    def reap_stale_slots(session: Session):
        """
        CRITICAL: The 'Reaper'. Finds slots where a worker crashed (is_busy=True
        but expires_at is in the past) and resets them.
        """
        now = datetime.datetime.utcnow()
        stmt = select(WorkerSlot).where(WorkerSlot.is_busy == True).where(WorkerSlot.expires_at < now)
        stale_slots = session.exec(stmt).all()

        for slot in stale_slots:
            slot.is_busy = False
            slot.current_dag_instance_id = None  # Task failed or needs retry
            session.add(slot)

        session.commit()
        return len(stale_slots)
