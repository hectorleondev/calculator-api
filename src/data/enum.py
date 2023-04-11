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


@unique
class RecordField(Enum):
    OPERATION_ID = "operation_id"
    AMOUNT = "amount"
    USER_BALANCE = "user_balance"
    OPERATION_RESPONSE = "operation_response"

    LIST = [
        OPERATION_ID,
        AMOUNT,
        USER_BALANCE,
        OPERATION_RESPONSE
    ]


@unique
class FilterType(Enum):
    LE = "le"
    LT = "lt"
    GE = "ge"
    GT = "gt"
    EQ = "eq"
    STARTWITH = "startswith"

    LIST = [
        LE,
        LT,
        GE,
        GT,
        EQ,
        STARTWITH
    ]

