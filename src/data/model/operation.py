import os
from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute)


class OperationModel(Model):
    """
    A model with an index
    """

    class Meta:
        table_name = os.getenv("OPERATION_TABLE")
        region = os.getenv("REGION", "us-east-1")

    operation_id = UnicodeAttribute(hash_key=True)
    type = UnicodeAttribute()
    cost = NumberAttribute(null=False, default=0.0)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())

    def to_dict(self):
        """
        Retrieves the model as a dictionary
        :return:
        """
        _dict_data = {
            "user_id": self.operation_id,
            "username": self.type,
            "user_balance": self.cost,
        }
        return _dict_data
