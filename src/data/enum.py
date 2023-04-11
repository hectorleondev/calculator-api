from enum import Enum, unique


@unique
class StatusType(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@unique
class OperationType(Enum):
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    SQUARE = "square_root"
    RANDOM = "random_string"
