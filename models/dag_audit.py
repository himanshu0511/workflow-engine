import datetime

class DagStatus:
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    TO_BE_EXECUTED = 'to_be_executed'

class DagAudit:
    dagId: str
    nodeId: str
    dagInstanceId: str
    nodeInstanceId: str
    inputKeyValueGroupId: str
    createdAt: datetime.datetime
    status: DagStatus
    retryCount: int
    nextRetryTime: datetime.datetime
    executionEndTime: datetime.datetime