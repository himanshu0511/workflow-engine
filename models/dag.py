import datetime
from enum import Enum


class DagType(str, Enum):
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return f"DagType.{self.name}"
    SCHEDULED = 'scheduled'
    ON_DEMAND = 'on_demand'

    def __init__(self, value):
        if value not in [self.SCHEDULED, self.ON_DEMAND]:
            raise ValueError(f"Invalid DagType: {value}")

class DAG:
    id: str
    type: DagType
    name: str
    description: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    cronString: str
    nextRun: datetime.datetime

