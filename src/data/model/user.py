import os

from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, BooleanAttribute, UTCDateTimeAttribute)
from datetime import datetime


class UserModel(Model):
    """
    A model with an index
    """

    class Meta:
        table_name = os.getenv("USER_TABLE")
        region = os.getenv("REGION", "us-east-1")

    user_id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)
    user_balance = NumberAttribute(null=False, default=0.0)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    status = UnicodeAttribute(null=False, default="active")
