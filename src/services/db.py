import uuid
from typing import List

from src.data.model.operation import OperationModel
from src.data.model.record import RecordModel
from src.data.model.user import UserModel
from pynamodb.exceptions import DoesNotExist


def create_user(username: str, password: str, email: str, user_balance: float):
    """
    Creqte new user
    :param username:
    :param password:
    :param email:
    :param user_balance:
    :return:
    """
    user = UserModel()
    user.user_id = str(uuid.uuid4().hex)
    user.username = username
    user.password = password
    user.email = email
    user.user_balance = user_balance
    user.save()


def search_user(username: str, password: str):
    """
    Search user by username and password
    :param username:
    :param password:
    :return:
    """
    return UserModel.username_password_index.query(
        hash_key=username,
        range_key_condition=password)


def get_user(user_id: str):
    """
    Get user
    :param user_id:
    :return:
    """
    try:
        return UserModel.get(hash_key=user_id)
    except DoesNotExist:
        return None


def create_operator(type_operation: str, cost: str):
    """
    Creqte new operation
    :param type_operation:
    :param cost:
    :return:
    """
    operation = OperationModel()
    operation.operation_id = str(uuid.uuid4().hex)
    operation.type = type_operation
    operation.cost = cost
    operation.save()


def get_all_operations():
    return OperationModel.scan()


def get_operation(operation_id):
    try:
        return OperationModel.get(hash_key=operation_id)
    except DoesNotExist:
        return None

def create_record(user_id: str,
                  operation_id: str,
                  operator_one: str,
                  operator_two: str,
                  operation_response: float):
    """
    Create record
    :param user_id:
    :param operation_id:
    :param operators:
    :param operation_response:
    :return:
    """

    record = RecordModel()
    record.user_id = user_id,
    record.operation_id = operation_id
    record.operation_response = str(operation_response)
    record.operator_one = operator_one
    record.operator_two = operator_two
    record.save()


def filter_record(user_id: str, operation_id: str, operation_response: str,
                  operation_one: str, operation_two: str, limit: int = 10,
                  last_evaluated_key = None):
    filter_condition = (RecordModel.user_id == user_id) & (RecordModel.is_active is True)
    if operation_id:
        filter_condition = filter_condition & (RecordModel.operation_id == operation_id)

    if operation_response:
        filter_condition = filter_condition & (RecordModel.operation_response.contains(operation_response))

    if operation_one:
        filter_condition = filter_condition & (RecordModel.operator_one.contains(operation_response))

    if operation_two:
        filter_condition = filter_condition & (RecordModel.operator_two.contains(operation_two))

    return RecordModel.scan(filter_condition=filter_condition, limit=limit,
                            last_evaluated_key=last_evaluated_key)


def get_record(record_id: str):
    try:
        return RecordModel.get(hash_key=record_id)
    except DoesNotExist:
        return None
