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
    operation_response = UnicodeAttribute(null=False)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())

    user_index = UserIndex()

    def to_dict(self):
        """
        Retrieves the model as a dictionary
        :return:
        """
        _dict_data = {
            "user_id": self.user_id,
            "operation_id": self.operation_id,
            "amount": self.amount,
            "user_balance": self.user_balance,
            "operation_response": self.operation_response
        }
        return _dict_data
