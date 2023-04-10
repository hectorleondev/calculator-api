from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute)

from src.services.config import ConfigService

conf = ConfigService()


class OperationModel(Model):
    """
    A model with an index
    """

    class Meta:
        table_name = conf.OPERATION_TABLE

    operation_id = UnicodeAttribute(hash_key=True)
    type = UnicodeAttribute()
    cost = NumberAttribute(null=False)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
