from enum import Enum


class DagStatus(str, Enum):
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    TO_BE_EXECUTED = 'to_be_executed'
