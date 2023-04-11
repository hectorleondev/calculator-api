import base64
import json
import os
from typing import List

import jwt
import requests

from src.data import schema
from src.data.data_type import FilterData
from src.data.enum import RecordField, FilterType
from src.data.exceptions import BadRequestException
from src.services.config import ConfigService

conf_service = ConfigService()


def get_content_json(filename: str) -> dict:
    """
    get json content
    :param filename:
    :return:
    """
    with open(f"{os.path.dirname(schema.__file__)}/{filename}.json") as f:
        data = json.load(f)
    return data


def encode_token(content: dict):
    """
    encode token
    :param content:
    :return:
    """
    return jwt.encode(content, conf_service.SECRET_JWT, algorithm="HS256")


def decode_token(token: str):
    """
    decode token
    :param token:
    :return:
    """
    return jwt.decode(token, conf_service.SECRET_JWT, algorithm="HS256")


def encrypt_password(password: str) -> str:
    password = password.encode('utf-8')
    return base64.b64encode(password).decode()


def get_random_string(length_string: str) -> requests.Response:
    headers = {"Content-Type": "application/json"}
    try:
        url = f"https://www.random.org/strings/?num=1&len={length_string}&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new"
        response = requests.post(url=url, headers=headers)
    except Exception as _:
        response = requests.models.Response()
        response.status_code = 404
    return response


def parse_filters(filter_param: str) -> List[FilterData]:
    filter_list: List[FilterData] = []
    if not filter_param:
        return filter_list

    items = filter_param.split(',')
    for item in items:
        params = item.split("+", 3)
        if len(params) < 3:
            raise BadRequestException("Invalid filters")

        if params[0] not in RecordField.LIST.value or params[1] not in FilterType.LIST.value:
            raise BadRequestException("Invalid filters")

        filter_list.append(FilterData.from_dict({
            "field": params[0],
            "operation": params[1],
            "value": params[2]
        }))
    return filter_list


def get_operation_dict(operations: list) -> dict:
    items = {}
    for operation in operations:
        items[operation["operation_id"]] = operation["type"]
    return items
