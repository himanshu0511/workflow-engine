from enum import Enum


class DagType(str, Enum):
    SCHEDULED = 'scheduled'
    ON_DEMAND = 'on_demand'