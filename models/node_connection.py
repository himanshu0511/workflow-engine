
class NodeConnection:
    dagId: str
    nodeId: str
    dependsOnNodeId: str

    @property
    def dependsOn(self) -> str:
        return self.dependsOnNodeId