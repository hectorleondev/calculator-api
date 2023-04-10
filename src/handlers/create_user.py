import json
from http import HTTPStatus

from aws_lambda_powertools import Logger
from src.services.config import ConfigService
from src.services.response import ResponseService
from src.services.validation import validate_event

conf = ConfigService()
logger = Logger(service=conf.LOGGER_SERVICE_NAME)


@ResponseService.pretty_response
def handler(event, _):
    logger.info({"message": "Event information", "event_info": event})

    body = json.loads(event.get("body", {}))

    validate_event(body, "create_user")

    return HTTPStatus.CREATED, body
