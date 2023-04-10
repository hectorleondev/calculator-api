from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, BooleanAttribute, UTCDateTimeAttribute)
from datetime import datetime
from pynamodb.indexes import (GlobalSecondaryIndex, AllProjection)

from src.services.config import ConfigService

conf = ConfigService()


class UsernamePasswordIndex(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()

    username = UnicodeAttribute(hash_key=True)
    password = UnicodeAttribute(range_key=True)


class UserModel(Model):
    """
    A model with an index
    """

    class Meta:
        table_name = conf.USER_TABLE

    user_id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    user_balance = NumberAttribute()
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    is_active = BooleanAttribute(default=True)

    username_password_index = UsernamePasswordIndex()
