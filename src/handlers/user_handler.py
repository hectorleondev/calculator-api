from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.controller.user_controller import UserController
from src.services.config import ConfigService
from src.services.response import ResponseService

conf = ConfigService()
logger = Logger(service=conf.LOGGER_SERVICE_NAME)


@ResponseService.pretty_response
def create_user_handler(event, _):

    user = UserController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.create_user()
    return HTTPStatus.CREATED, response


@ResponseService.pretty_response
def update_user_handler(event, _):

    user = UserController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.update_user()
    return HTTPStatus.OK, response


@ResponseService.pretty_response
def login_user_handler(event, _):

    user = UserController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.login_user()
    return HTTPStatus.OK, response


@ResponseService.pretty_response
def delete_user_handler(event, _):

    user = UserController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.delete_user()
    return HTTPStatus.OK, response

