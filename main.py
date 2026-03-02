# main.py
from fastapi import FastAPI
from api import dag_router, node_router, node_dependencies_router

app = FastAPI()

# Include the routers
app.include_router(dag_router, prefix="/workflow", tags=["dag"])
app.include_router(node_router, prefix="/workflow", tags=["node"])
app.include_router(node_dependencies_router, prefix="/workflow", tags=["node_dependencies"])

@app.get("/")
async def root():
    return {"message": "Main Application Entry"}
