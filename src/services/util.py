import base64
import json
import os

import jwt
import requests

from src.data import schema
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
