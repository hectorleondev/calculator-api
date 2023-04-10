from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, BooleanAttribute, UTCDateTimeAttribute)
from datetime import datetime
from pynamodb.indexes import (GlobalSecondaryIndex, AllProjection)

from src.services.config import ConfigService

conf = ConfigService()


class UserModel(Model):
    """
    A model with an index
    """

    class Meta:
        table_name = "calculator-api-dev-UserTable-10M75T9OTA2I8"
        region = 'us-east-1'
        host = 'https://dynamodb.us-east-1.amazonaws.com'

    user_id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)
    user_balance = NumberAttribute()
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    is_active = BooleanAttribute(default=True)

    def save(self, conditional_operator=None, **expected_values):
        self.createdAt = datetime.now()
        self.is_active = True
        super(UserModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
