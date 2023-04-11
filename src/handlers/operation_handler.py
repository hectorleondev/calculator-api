from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.controller.operation_controller import OperationController
from src.services.config import ConfigService
from src.services.response import ResponseService

conf = ConfigService()
logger = Logger(service=conf.LOGGER_SERVICE_NAME)


@ResponseService.pretty_response
def create_operation_handler(event, _):

    user = OperationController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.create_operation()
    return HTTPStatus.CREATED, response


@ResponseService.pretty_response
def update_operation_handler(event, _):

    user = OperationController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.update_operation()
    return HTTPStatus.OK, response


@ResponseService.pretty_response
def get_operation_list_handler(event, _):

    user = OperationController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.get_operation_list()
    return HTTPStatus.OK, response



