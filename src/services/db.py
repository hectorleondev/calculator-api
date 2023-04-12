import uuid
from typing import List

from src.data.data_type import FilterData
from src.data.enum import StatusType, RecordField, FilterType
from src.data.model.operation import OperationModel
from src.data.model.record import RecordModel
from src.data.model.user import UserModel
from pynamodb.exceptions import DoesNotExist


def create_user(user_id: str, username: str, user_balance: float):
    """
    Creqte new user
    :param user_id:
    :param username:
    :param user_balance:
    :return:
    """
    user = UserModel(user_id=user_id,
                     username=username,
                     user_balance=user_balance)
    user.save()


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


def get_all_operation(items: list, filter_condition: any, operation_list: dict, limit: int = 100, last_evaluated_key=None)\
        -> list:

    response = RecordModel.scan(filter_condition=filter_condition,
                                last_evaluated_key=last_evaluated_key,
                                limit=limit)

    for item in response:
        new_item = item.to_dict()
        new_item["operation_type"] = operation_list[item.operation_id]
        items.append(new_item)

    if response.last_evaluated_key:
        items = get_all_operation(items=items,
                                  operation_list=operation_list,
                                  filter_condition=filter_condition,
                                  last_evaluated_key=response.last_evaluated_key)
    return items


def get_records_using_filter(filters: List[FilterData], user_id: str, operation_list: dict) -> list:
    """

    :param filters:
    :param user_id:
    :param operation_list:
    :return:
    """
    filter_operation_id = None
    filter_operation_response = None
    filter_operation_amount = None
    filter_user_balance = None
    for item in filters:
        if item.field == RecordField.OPERATION_ID.value:
            filter_operation_id = RecordModel.operation_id == item.value

        if item.field == RecordField.OPERATION_RESPONSE.value:
            if item.operation == FilterType.EQ.value:
                filter_operation_response = RecordModel.operation_response == str(item.value)
            if item.operation == FilterType.STARTWITH.value:
                filter_operation_response = RecordModel.operation_response.startswith(str(item.value))

        if item.field == RecordField.AMOUNT.value:
            if item.operation == FilterType.EQ.value:
                filter_operation_amount = RecordModel.amount == float(item.value)
            if item.operation == FilterType.LE.value:
                filter_operation_amount = RecordModel.amount <= float(item.value)
            if item.operation == FilterType.LT.value:
                filter_operation_amount = RecordModel.amount < float(item.value)
            if item.operation == FilterType.GE.value:
                filter_operation_amount = RecordModel.amount >= float(item.value)
            if item.operation == FilterType.GT.value:
                filter_operation_amount = RecordModel.amount > float(item.value)

        if item.field == RecordField.USER_BALANCE.value:
            if item.operation == FilterType.EQ.value:
                filter_user_balance = RecordModel.user_balance == float(item.value)
            if item.operation == FilterType.LE.value:
                filter_user_balance = RecordModel.user_balance <= float(item.value)
            if item.operation == FilterType.LT.value:
                filter_user_balance = RecordModel.user_balance < float(item.value)
            if item.operation == FilterType.GE.value:
                filter_user_balance = RecordModel.user_balance >= float(item.value)
            if item.operation == FilterType.GT.value:
                filter_user_balance = RecordModel.user_balance > float(item.value)

    filter_condition = (RecordModel.user_id == user_id)

    if filter_user_balance is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance)

    if filter_operation_amount is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_operation_amount)

    if filter_operation_id is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_operation_id)

    if filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_operation_response)

    if filter_user_balance is not None and filter_operation_amount is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance) & (filter_operation_amount)

    if filter_user_balance is not None and filter_operation_id is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance) & (filter_operation_id)

    if filter_user_balance is not None and filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance) & (filter_operation_response)

    if filter_operation_amount is not None and filter_operation_id is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_operation_amount) & (filter_operation_id)

    if filter_operation_amount is not None and filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_operation_amount) & (filter_operation_response)

    if filter_operation_id is not None and filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_operation_id) & (filter_operation_response)

    if filter_user_balance is not None and filter_operation_amount is not None and filter_operation_id is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance) & (filter_operation_amount) & (filter_operation_id)

    if filter_user_balance is not None and filter_operation_amount is not None and filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance) & (filter_operation_amount) & (filter_operation_response)

    if filter_user_balance is not None and filter_operation_id is not None and filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance) & (filter_operation_id) & (filter_operation_response)

    if filter_operation_amount is not None and filter_operation_id is not None and filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_operation_amount) & (filter_operation_id) & (filter_operation_response)

    if filter_user_balance is not None and filter_operation_amount is not None and filter_operation_id is not None and filter_operation_response is not None:
        filter_condition = (RecordModel.user_id == user_id) & (filter_user_balance) & (filter_operation_amount) & (filter_operation_id) & (filter_operation_response)

    return get_all_operation(items=[], filter_condition=filter_condition, operation_list=operation_list)
