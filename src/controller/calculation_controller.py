import json
import math
from typing import Any

from src.data.enum import OperationType
from src.data.exceptions import BadRequestException
from src.services.config import ConfigService
from aws_lambda_powertools import Logger

from src.services.db import get_user, get_operation, create_record, update_user_balance
from src.services.validation import validate_event


class CalculationController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_calculation(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        validate_event(body, "create_calculation")

        user_id = body.get("user_id", "")

        user = get_user(user_id)
        if not user:
            raise BadRequestException("There is not an account with user_id")

        operation_id = body.get("operation_id", "")

        operation = get_operation(operation_id)
        if not operation:
            raise BadRequestException("There is not an operation with operation_id")

        new_balance = user.user_balance - operation.cost
        if new_balance <= 0:
            raise BadRequestException("User’s balance isn’t enough to cover the request cost")

        operation_response = None
        amount_one = body.get("amount_one", "")
        amount_two = body.get("amount_two", "")

        if operation.type == OperationType.ADDITION:
            if not amount_one or not amount_two:
                raise BadRequestException("amount_one and amount_two are required")
            operation_response = str(float(amount_one) + float(amount_two))

        if operation.type == OperationType.SUBTRACTION:
            if not amount_one or not amount_two:
                raise BadRequestException("amount_one and amount_two are required")
            operation_response = str(float(amount_one) - float(amount_two))

        if operation.type == OperationType.MULTIPLICATION:
            if not amount_one or not amount_two:
                raise BadRequestException("amount_one and amount_two are required")
            operation_response = str(float(amount_one) * float(amount_two))

        if operation.type == OperationType.DIVISION:
            if not amount_one or not amount_two:
                raise BadRequestException("amount_one and amount_two are required")
            amount_two = float(amount_two)
            if amount_two == 0:
                raise BadRequestException("The amount two must be different from zero")
            operation_response = str(float(amount_one) / amount_two)

        if operation.type == OperationType.SQUARE:
            if not amount_one:
                raise BadRequestException("amount_one is required")
            operation_response = str(math.sqrt(float(amount_one)))

        if not operation_response:
            raise BadRequestException("The operation does not logic")

        create_record(user_id=user_id,
                      operation_id=operation_id,
                      amount=operation.cost,
                      user_balance=new_balance,
                      operation_response=operation_response)

        update_user_balance(user, new_balance)

        return {"message": "Calculation was created successfully"}



