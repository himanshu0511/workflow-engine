import random
from uuid import UUID

from fastapi import APIRouter

# Create the router instance
router = APIRouter()

@router.get("/dag/{dag_id}/node/")
async def list_nodes(dag_id: str):
    return [{"dagId": dag_id, "id": "node1"}, {"dagId": dag_id, "id": "node2"}]

@router.get("/dag/{dag_id}/node/{node_id}/")
async def list_nodes(dag_id: str, node_id: str):
    return {"dagId": dag_id, "id": node_id}

@router.post("/dag/{dag_id}/node/")
def create_node(dag_id: str):
    node_id = UUID(int=random.getrandbits(128))
    return {"dagId": dag_id, "id":node_id}

@router.put("/dag/{dag_id}/node/{node_id}/")
def update_node(dag_id: str, node_id: str):
    return {"dagId": dag_id, "id": node_id}

@router.delete("/dag/{dag_id}/node/{node_id}/")
def delete_node(dag_id: str, node_id: str):
    return {"dagId": dag_id, "id": node_id}

