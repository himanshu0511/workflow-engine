# api/dag.py
import random
from uuid import UUID

from fastapi import APIRouter

# Create the router instance
router = APIRouter()

@router.get("/dag/")
async def list_dags():
    return [{"id": "dag1"}, {"id": "dag2"}]

@router.get("/dag/{id}")
async def get_dag(id):
    return {"id":id}

@router.post("/dag/")
async def create_dag():
    return {"id": "new_dag_id"}

@router.put("/dag/{id}")
async def update_dag(id):
    return {"id": id}

@router.delete("/dag/{id}")
async def delete_dag(id):
    return {"id": id}

@router.post("/dag/{id}/trigger")
async def trigger_dag(id):
    instanceId = UUID(int=random.getrandbits(128))
    return {"message": f"Triggered DAG Instance: {instanceId} of DAG: {id}"}

@router.get("/dag/{instance_id}/status")
async def get_dag_status(instance_id):
    return {id: "dagId1", "instance_id": instance_id, "status": "running"}

@router.post("/dag/{instance_id}/pause")
async def pause_dag(instance_id):
    return {"id": "dagId1","instance_id": instance_id, "message": f"Paused DAG: {instance_id}"}

@router.post("/dag/{instance_id}/resume")
async def resume_dag(instance_id):
    return {"id": "dagId1","instance_id": instance_id, "message": f"Resumed DAG: {instance_id}"}

@router.post("/dag/{instance_id}/retry")
async def retry_dag(instance_id):
    return {"id": "dagId1","instance_id": instance_id, "message": f"Retried DAG: {instance_id}"}

@router.post("/dag/{instance_id}/stop")
async def stop_dag(instance_id):
    return {"id": "dagId1","instance_id": instance_id, "message": f"Stopped DAG: {instance_id}"}

