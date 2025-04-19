from enum import Enum


class VerdictType(Enum):
    MALICIOUS = "MALICIOUS"
    BENIGN = "BENIGN"
    UNKNOWN = "UNKNOWN"