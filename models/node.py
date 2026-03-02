import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

# values def/condional/exec/network/email/sms/whatsapp
class NodeType(str, Enum):
    def __str__(self):
        return self.value
    def __repr__(self):
        return f"NodeType.{self.name}"
    DEF = 'def'
    COND = 'cond'
    EXEC = 'exec'
    NETWORK = 'network'
    EMAIL = 'email'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'

class RetryType(str, Enum):
    def __str__(self):
        return self.value
    def __repr__(self):
        return f"RetryType.{self.name}"
    NONE = 'none'
    FIXED = 'fixed'
    EXPONENTIAL = 'exponential'
    LINEAR = 'linear'

class Node:
    id: str
    type: NodeType
    dagId: str
    source: str
    retryType: RetryType
    initialDelay: int
    maxDelay: int
    factor: float
    maxRetries: int
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)