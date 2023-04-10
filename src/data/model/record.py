from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute, ListAttribute)
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
        table_name = conf.RECORD_TABLE

    record_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute()
    operation_id = UnicodeAttribute()
    operator_one = UnicodeAttribute(null=False)
    operator_two = UnicodeAttribute()
    operation_response = UnicodeAttribute()
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    is_active = BooleanAttribute(default=True)

    user_index = UserIndex()
