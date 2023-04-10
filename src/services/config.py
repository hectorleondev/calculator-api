import os


class ConfigService:
    def __init__(self):
        self.USER_TABLE: str = os.getenv("USER_TABLE")
        self.OPERATION_TABLE: str = os.getenv("OPERATION_TABLE")
        self.RECORD_TABLE: str = os.getenv("RECORD_TABLE")
        self.LOGGER_SERVICE_NAME: str = os.getenv("LOGGER_SERVICE_NAME")

