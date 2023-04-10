import os


class ConfigService:
    def __init__(self):
        self.LOGGER_SERVICE_NAME: str = os.getenv("LOGGER_SERVICE_NAME")
        self.SECRET_JWT = "31c442545ba548899491635bdc33b00f"
