import uuid

from src.data.enum import StatusType
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
    return UserModel.scan(filter_condition=(UserModel.username == username) &
                                           (UserModel.password == password) &
                                           (UserModel.status == StatusType.ACTIVE.value))


def get_user_by_email(email: str):
    """
    Get user
    :param email:
    :return:
    """
    return UserModel.scan(filter_condition=(UserModel.username == email) &
                                           (UserModel.status == StatusType.ACTIVE.value))


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
                  amount: float,
                  user_balance: float,
                  operation_response: float):
    """
    Create record
    :param user_id:
    :param operation_id:
    :param amount:
    :param user_balance:
    :param operation_response:
    :return:
    """

    record = RecordModel(user_id=user_id,
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

