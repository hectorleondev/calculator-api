import os

import pytest


@pytest.fixture(scope="session")
def aws_env_vars():
    """Testing AWS Credentials."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing_key_id"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing_access_key"
    os.environ["AWS_SECURITY_TOKEN"] = "testing_security_token"
    os.environ["AWS_SESSION_TOKEN"] = "testing_session_token"
    os.environ["REGION"] = "us-east-1"
    os.environ["ACCESS_PROCESSING_QUEUE"] = "access_queue_name"
    os.environ["ACCESS_KEYS_TABLE"] = "accesskeytesttable"
    os.environ["CLIENT_ID"] = ""
    os.environ["USER_POOL_ID"] = ""
    os.environ["CUSTOM_POOL_DOMAIN"] = ""
    os.environ["CALLBACK_URL"] = "https://test.test.com/access/callback"
    os.environ["ADMIN_GROUP"] = "testing-admin-group"
    os.environ["UNCONFIRMED_GROUP"] = "testing-unconfirmed-group"
    os.environ["CONFIRMED_GROUP"] = "testing-confirmed-group"
    os.environ["DOMAIN_NAME_ROOT"] = "testing.test.com"

