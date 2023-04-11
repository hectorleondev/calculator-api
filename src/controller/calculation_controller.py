import json
from http import HTTPStatus

import math
from typing import Any

from src.data.enum import OperationType
from src.data.exceptions import BadRequestException, NotFoundException
from src.services.config import ConfigService
from aws_lambda_powertools import Logger

from src.services.db import get_user, get_operation, create_record, update_user_balance
from src.services.util import get_random_string
from src.services.validation import validate_event


class CalculationController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_calculation(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        user_id = body.get("user_id", "")

        user = get_user(user_id)
        if not user:
            raise BadRequestException("There is not an account with user_id")

        operation_id = body.get("operation_id", "")

        operation = get_operation(operation_id)
        if not operation:
            raise BadRequestException("There is not an operation with operation_id")

        validate_event(body, f"create_calculation_{operation.type}")

        new_balance = user.user_balance - operation.cost
        if new_balance <= 0:
            raise BadRequestException("User’s balance isn’t enough to cover the request cost")

        operation_response = None
        if operation.type == OperationType.ADDITION.value:
            operation_response = str(float(body.get("addend_one")) + float(body.get("addend_two")))

        if operation.type == OperationType.SUBTRACTION.value:
            operation_response = str(float(body.get("minuend")) - float(body.get("subtrahend")))

        if operation.type == OperationType.MULTIPLICATION.value:
            operation_response = str(float(body.get("multiplicand")) * float(body.get("multiplier")))

        if operation.type == OperationType.DIVISION.value:
            operation_response = str(float(body.get("dividend")) / float(body.get("divisor")))

        if operation.type == OperationType.SQUARE.value:
            operation_response = str(math.sqrt(float(body.get("radicand"))))

        if operation.type == OperationType.RANDOM.value:
            response = get_random_string(body.get("length_string"))
            if response.status_code != HTTPStatus.OK:
                raise NotFoundException("Resource not found")
            operation_response = response.text

        if not operation_response:
            raise BadRequestException("The operation does not logic")

        create_record(user_id=user_id,
                      operation_id=operation_id,
                      amount=operation.cost,
                      user_balance=new_balance,
                      operation_response=operation_response)

        update_user_balance(user, new_balance)

        return {"message": "Calculation was created successfully"}



