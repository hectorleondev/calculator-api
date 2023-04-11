import uuid
from typing import List

from src.data.data_type import FilterData
from src.data.enum import StatusType, RecordField, FilterType
from src.data.model.operation import OperationModel
from src.data.model.record import RecordModel
from src.data.model.user import UserModel
from pynamodb.exceptions import DoesNotExist


def create_user(username: str, password: str, user_balance: float):
    """
    Creqte new user
    :param username:
    :param password:
    :param user_balance:
    :return:
    """
    user = UserModel(user_id=str(uuid.uuid4()),
                     username=username,
                     password=password,
                     user_balance=user_balance)
    user.save()


def search_user(username: str, password: str):
    """
    Search user by username and password
    :param username:
    :param password:
    :return:
    """
    try:
        _users = list(UserModel.scan(filter_condition=(UserModel.username == username) &
                                                      (UserModel.password == password) &
                                                      (UserModel.status == StatusType.ACTIVE.value)))
    except UserModel.DoesNotExist:
        _users = []
    _users = [_key.to_dict() for _key in _users]
    return _users


def get_user_by_email(email: str):
    """
    Get user
    :param email:
    :return:
    """
    try:
        _users = list(UserModel.scan(filter_condition=(UserModel.username == email) &
                                       (UserModel.status == StatusType.ACTIVE.value)))
    except UserModel.DoesNotExist:
        _users = []
    _users = [_key.to_dict() for _key in _users]
    return _users


def get_user(user_id: str):
    """
    Get user
    :param user_id:
    :return:
    """
    try:
        return UserModel.get(hash_key=user_id)
    except UserModel.DoesNotExist:
        return None


def remove_user(instance: UserModel):
    instance.status = StatusType.INACTIVE.value
    instance.save()


def update_user_balance(instance: UserModel, balance: float):
    instance.user_balance = balance
    instance.save()


def create_operator(type_operation: str, cost: float):
    """
    Creqte new operation
    :param type_operation:
    :param cost:
    :return:
    """
    operation = OperationModel()
    operation.operation_id = str(uuid.uuid4())
    operation.type = type_operation
    operation.cost = cost
    operation.save()


def update_operator(instance: OperationModel, cost: float):
    """
    Update operation
    :param instance:
    :param cost:
    :return:
    """
    instance.cost = cost
    instance.save()


def get_all_operations():
    try:
        _operations = list(OperationModel.scan())
    except OperationModel.DoesNotExist:
        _operations = []
    _operations = [_key.to_dict() for _key in _operations]
    return _operations


def get_operation(operation_id):
    try:
        return OperationModel.get(hash_key=operation_id)
    except OperationModel.DoesNotExist:
        return None


def get_operation_by_type(type_operation: str):
    """
    Get user
    :param type_operation:
    :return:
    """
    try:
        _operations = list(OperationModel.scan(filter_condition=(OperationModel.type == type_operation)))
    except OperationModel.DoesNotExist:
        _operations = []
    _operations = [_key.to_dict() for _key in _operations]
    return _operations


def create_record(user_id: str,
                  operation_id: str,
                  amount: float,
                  user_balance: float,
                  operation_response: str):
    """
    Create record
    :param user_id:
    :param operation_id:
    :param amount:
    :param user_balance:
    :param operation_response:
    :return:
    """

    record = RecordModel(record_id=str(uuid.uuid4()),
                         user_id=user_id,
                         operation_id=operation_id,
                         amount=amount,
                         user_balance=user_balance,
                         operation_response=operation_response)
    record.save()


def get_record(record_id: str):
    try:
        return RecordModel.get(hash_key=record_id)
    except DoesNotExist:
        return None


def get_all_operation(items: list, filter_condition: any, limit: int = 100, last_evaluated_key=None)\
        -> list:

    response = RecordModel.scan(filter_condition=filter_condition,
                                last_evaluated_key=last_evaluated_key,
                                limit=limit)

    for item in response:
        items.append(item)

    if response.last_evaluated_key:
        items = get_all_operation(items=items,
                                  filter_condition=filter_condition,
                                  last_evaluated_key=response.last_evaluated_key)
    return items


def get_records_using_filter(filters: List[FilterData], user_id: str) -> list:
    """

    :param filters:
    :param user_id:
    :return:
    """
    filter_condition = RecordModel.user_id == user_id
    for item in filters:
        if item.field == RecordField.OPERATION_ID.value:
            filter_condition &= RecordModel.operation_id == item.value

        if item.field == RecordField.OPERATION_RESPONSE.value:
            if item.operation == FilterType.EQ.value:
                filter_condition &= RecordModel.operation_response == str(item.value)
            if item.operation == FilterType.STARTWITH.value:
                filter_condition &= RecordModel.operation_response.startswith(str(item.value))

        if item.field == RecordField.AMOUNT.value:
            if item.operation == FilterType.EQ.value:
                filter_condition &= RecordModel.amount == float(item.value)
            if item.operation == FilterType.LE.value:
                filter_condition &= RecordModel.amount <= float(item.value)
            if item.operation == FilterType.LT.value:
                filter_condition &= RecordModel.amount < float(item.value)
            if item.operation == FilterType.GE.value:
                filter_condition &= RecordModel.amount >= float(item.value)
            if item.operation == FilterType.GT.value:
                filter_condition &= RecordModel.amount > float(item.value)

        if item.field == RecordField.USER_BALANCE.value:
            if item.operation == FilterType.EQ.value:
                filter_condition &= RecordModel.user_balance == float(item.value)
            if item.operation == FilterType.LE.value:
                filter_condition &= RecordModel.user_balance <= float(item.value)
            if item.operation == FilterType.LT.value:
                filter_condition &= RecordModel.user_balance < float(item.value)
            if item.operation == FilterType.GE.value:
                filter_condition &= RecordModel.user_balance >= float(item.value)
            if item.operation == FilterType.GT.value:
                filter_condition &= RecordModel.user_balance > float(item.value)

    return get_all_operation(items=[], filter_condition=filter_condition)



