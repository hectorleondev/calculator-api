import json
from typing import Any

from src.data.exceptions import BadRequestException
from src.services.config import ConfigService
from aws_lambda_powertools import Logger

from src.services.db import get_user_by_email, create_user
from src.services.util import encrypt_password
from src.services.validation import validate_event


class UserController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_user(self):
        self.logger.info({"message": "Event information", "event_info": event})

        body = json.loads(self.event.get("body", {}))

        validate_event(body, "create_user")

        email = body.get("username", "")

        users = get_user_by_email(email)
        if users.total_count > 0:
            raise BadRequestException("There is an account with that username")

        password = encrypt_password(body.get("password", ""))
        user_balance = float(body.get("user_balance", "0"))

        create_user(email, password, user_balance)

        return {"message": "User was created successfully"}