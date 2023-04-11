import json
from typing import Any

from src.data.exceptions import BadRequestException
from src.services.config import ConfigService
from aws_lambda_powertools import Logger

from src.services.db import get_user_by_email, create_user, search_user, get_user, update_user_balance, remove_user, \
    get_operation, create_operator, get_all_operations, update_operator, get_operation_by_type
from src.services.util import encrypt_password
from src.services.validation import validate_event


class OperationController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_operation(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        validate_event(body, "create_operation")

        type_operation = body.get("type", "")

        operation = get_operation_by_type(type_operation)
        if operation:
            raise BadRequestException("There is an operation with that type")

        cost = float(body.get("cost", "0"))

        if cost <= 0:
            raise BadRequestException("The cost must be greater than zero")

        create_operator(type_operation, cost)

        return {"message": "Operation was created successfully"}

    def get_operation_list(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        operations = get_all_operations()

        return {"operations": operations}

    def update_operation(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        validate_event(body, "update_operation")

        operation_id = self.event.get("pathParameters", {}).get("operation_id", "")

        operation = get_operation(operation_id)
        if not operation:
            raise BadRequestException("There is not an operation with operation_id")

        cost = float(body.get("cost", "0"))

        if cost <= 0:
            raise BadRequestException("The cost must be greater than zero")

        update_operator(operation, cost)

        return {"message": "Operation was updated successfully"}


