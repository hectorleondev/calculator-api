import os

import boto3


class ConfigService:
    def __init__(self):
        self.LOGGER_SERVICE_NAME: str = os.getenv("LOGGER_SERVICE_NAME")
        self.SECRET_JWT = "31c442545ba548899491635bdc33b00f"
        self.REGION: str = os.getenv("REGION", "us-east-1")
        self.cognito_cli = boto3.client("cognito-idp", region_name=self.REGION)
        self.CLIENT_ID: str = os.getenv("USER_POOL_CLIENT_ID", "")
        self.USER_POOL_ID: str = os.getenv("USER_POOL_ID", "")