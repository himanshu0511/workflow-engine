from enum import Enum


# values def/condional/exec/network/email/sms/whatsapp
class ExecutionType(str, Enum):
    DEF = 'def'
    COND = 'cond'
    EXEC = 'exec'
    NETWORK = 'network'
    EMAIL = 'email'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'