from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.controller.user_controller import UserController
from src.services.config import ConfigService
from src.services.response import ResponseService

conf = ConfigService()
logger = Logger(service=conf.LOGGER_SERVICE_NAME)


@ResponseService.pretty_response
def handler(event, _):

    user = UserController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.login_user()
    return HTTPStatus.OK, response
