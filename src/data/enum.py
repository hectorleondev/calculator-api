from enum import Enum, unique


@unique
class StatusType(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
