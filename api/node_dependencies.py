from fastapi import APIRouter

# Create the router instance
router = APIRouter()

@router.get("/dag/{dag_id}/dependencies/")
async def list_nodes(dag_id: str):
    return [{"dagId": dag_id, "id": "node1", "dependsOnNodeId": None}, {"dagId": dag_id, "id": "node2", "dependsOnNodeId": "node1"}]

@router.get("/dag/{dag_id}/dependencies/{node_id}")
async def get_node(dag_id: str, node_id: str):
    return {"dagId": dag_id, "id": node_id, "dependsOnNodeId": "dependOnNodeId1"}

@router.post("/dag/{dag_id}/dependencies/{node_id}/add_dependency/{depends_on_node_id}")
async def add_dependency(dag_id: str, node_id: str, depends_on_node_id: str):
    return {"dagId": dag_id, "id": node_id, "dependsOnNodeId": depends_on_node_id}

@router.delete("/dag/{dag_id}/dependencies/{node_id}/remove_dependency/{depends_on_node_id}")
async def remove_dependency(dag_id: str, node_id: str):
    return {"dagId": dag_id, "id": node_id, "dependsOnNodeId": None}