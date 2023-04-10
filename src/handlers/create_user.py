import json
from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.data.exceptions import BadRequestException
from src.services.config import ConfigService
from src.services.db import get_user_by_email, create_user
from src.services.response import ResponseService
from src.services.util import encrypt_password
from src.services.validation import validate_event

conf = ConfigService()
logger = Logger(service=conf.LOGGER_SERVICE_NAME)


@ResponseService.pretty_response
def handler(event, _):
    logger.info({"message": "Event information", "event_info": event})

    body = json.loads(event.get("body", {}))

    validate_event(body, "create_user")

    email = body.get("username", "")

    users = get_user_by_email(email)
    if users:
        raise BadRequestException("There is an account with that username")

    password = encrypt_password(body.get("password", ""))
    user_balance = float(body.get("user_balance", 0))

    create_user(email, password, user_balance)

    return HTTPStatus.CREATED, {"message": "User was created successfully"}
