from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.controller.operation_controller import OperationController
from src.services.config import ConfigService
from src.services.response import ResponseService


@ResponseService.pretty_response
def create_operation_handler(event, context, conf_svc: ConfigService, logger: Logger):
    operation = OperationController(_conf_svc=conf_svc, _event=event, _logger=logger)
    response = operation.create_operation()
    return HTTPStatus.CREATED, response


@ResponseService.pretty_response
def update_operation_handler(event, context, conf_svc: ConfigService, logger: Logger):
    operation = OperationController(_conf_svc=conf_svc, _event=event, _logger=logger)
    response = operation.update_operation()
    return HTTPStatus.OK, response


@ResponseService.pretty_response
def get_operation_list_handler(event, context, conf_svc: ConfigService, logger: Logger):
    operation = OperationController(_conf_svc=conf_svc, _event=event, _logger=logger)
    response = operation.get_operation_list()
    return HTTPStatus.OK, response
