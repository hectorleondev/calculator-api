from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.controller.calculation_controller import CalculationController
from src.services.config import ConfigService
from src.services.response import ResponseService

conf = ConfigService()
logger = Logger(service=conf.LOGGER_SERVICE_NAME)


@ResponseService.pretty_response
def create_calculation_handler(event, _):

    user = CalculationController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.create_calculation()
    return HTTPStatus.CREATED, response


@ResponseService.pretty_response
def get_calculation_handler(event, _):

    user = CalculationController(_conf_svc=conf, _event=event, _logger=logger)
    response = user.retrieve_calculation()
    return HTTPStatus.OK, response
