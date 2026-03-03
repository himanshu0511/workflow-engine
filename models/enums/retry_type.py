from enum import Enum


class RetryType(str, Enum):
    NONE = 'none'
    FIXED = 'fixed'
    EXPONENTIAL = 'exponential'
    LINEAR = 'linear'
