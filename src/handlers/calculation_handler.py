from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.controller.calculation_controller import CalculationController
from src.services.config import ConfigService
from src.services.response import ResponseService


@ResponseService.pretty_response
def create_calculation_handler(event, context, conf_svc: ConfigService, logger: Logger):
    calculation = CalculationController(_conf_svc=conf_svc, _event=event, _logger=logger)
    response = calculation.create_calculation()
    return HTTPStatus.CREATED, response


@ResponseService.pretty_response
def get_calculation_handler(event, context, conf_svc: ConfigService, logger: Logger):
    calculation = CalculationController(_conf_svc=conf_svc, _event=event, _logger=logger)
    response = calculation.retrieve_calculation()
    return HTTPStatus.OK, response
