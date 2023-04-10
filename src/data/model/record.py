import os

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute)
from datetime import datetime
from pynamodb.indexes import (GlobalSecondaryIndex, AllProjection)

from src.services.config import ConfigService

conf = ConfigService()


class UserIndex(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()

    user_id = UnicodeAttribute(hash_key=True)


class RecordModel(Model):
    """
    A model with an index
    """

    class Meta:
        table_name = os.getenv("RECORD_TABLE")
        region = os.getenv("REGION", "us-east-1")

    record_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(null=False)
    operation_id = UnicodeAttribute(null=False)
    amount = NumberAttribute(null=False, default=0.0)
    user_balance = NumberAttribute(null=False, default=0.0)
    operation_response = NumberAttribute(null=False, default=0.0)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())

    user_index = UserIndex()
