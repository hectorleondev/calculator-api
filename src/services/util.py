import json
import os

import bcrypt
import jwt

from src.data import schema
from src.services.config import ConfigService

conf_service = ConfigService()


def get_content_json(filename: str):
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


def encrypt_password(password: str):
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())