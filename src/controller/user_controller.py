import json
from typing import Any

from src.data.exceptions import BadRequestException
from src.services.cognito import sign_up, admin_confirm_sign_up, authenticate_user
from src.services.config import ConfigService
from aws_lambda_powertools import Logger

from src.services.db import get_user_by_email, create_user, get_user, update_user_balance, remove_user
from src.services.validation import validate_event


class UserController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_user(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        validate_event(body, "create_user")

        email = body.get("username", "")

        users = get_user_by_email(email)
        if users:
            raise BadRequestException("There is an account with that username")

        password = body.get("password", "")
        user_id = sign_up(
            cognito_cli=self.conf_svc.cognito_cli,
            cognito_client_id=self.conf_svc.CLIENT_ID,
            password=password,
            email=email
        )

        admin_confirm_sign_up(
            cognito_cli=self.conf_svc.cognito_cli,
            user_pool_id=self.conf_svc.USER_POOL_ID,
            username=email
        )

        user_balance = float(body.get("user_balance", "0"))

        create_user(user_id, email, user_balance)

        user_info = {
            "user_id": user_id,
            "username": email,
            "user_balance": user_balance
        }

        return {"user_info": user_info}

    def login_user(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        validate_event(body, "login")

        email = body.get("username", "")
        password = body.get("password", "")

        _authenticated_data = authenticate_user(
            cognito_cli=self.conf_svc.cognito_cli,
            cognito_client_id=self.conf_svc.CLIENT_ID,
            email=email,
            password=password,
        )
        return {"token": _authenticated_data.get("id_token")}

    def get_user_info(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        # validate_event(body, "login")
        #
        # email = body.get("username", "")
        # password = encrypt_password(body.get("password", ""))
        #
        # users = search_user(email, password)
        # if not users:
        #     raise BadRequestException("Account not found")

        # return {"user": users[0]}

    def update_user(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        validate_event(body, "update_user")

        user_id = self.event.get("pathParameters", {}).get("user_id", "")

        user = get_user(user_id)
        if not user:
            raise BadRequestException("There is not an account with user_id")

        user_balance = float(body.get("user_balance", "0"))

        if user.user_balance >= user_balance:
            raise BadRequestException("The new balance must be greater than previous one")

        update_user_balance(user, user_balance)

        return {"message": "User was updated successfully"}

    def delete_user(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        user_id = self.event.get("pathParameters", {}).get("user_id", "")

        user = get_user(user_id)
        if not user:
            raise BadRequestException("There is not an account with user_id")

        remove_user(user)

        return {"message": "User was removed successfully"}

