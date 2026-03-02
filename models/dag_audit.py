import datetime


class DagAudit:
    dagId: str
    dagInstanceId: str
    nodeId: str
    nodeInstanceId: str
    inputKeyValueGroupId: str
    createdAt: datetime.datetime
    executionStatus: str
    executionEndTime: datetime.datetime