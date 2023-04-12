from botocore import exceptions as boto_exceptions
from src.data.exceptions import UserNotFound, UserNotConfirmed, InvalidCredentials
from aws_lambda_powertools import Logger


def get_exceptions(cognito_cli):
    """

    :param cognito_cli:
    :return:
    """
    return cognito_cli.exceptions


def sign_up(cognito_cli, cognito_client_id, email, password):
    """

    :param cognito_cli:
    :param cognito_client_id:
    :param email:
    :param password:
    :return:
    """
    try:
        new_user_response = cognito_cli.sign_up(
            ClientId=cognito_client_id,
            Username=email,
            Password=password,
            UserAttributes=[],
        )
        return new_user_response.get("UserSub")
    except boto_exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "UsernameExistsException":
            raise error
        else:
            Logger.exception("An unexpected error has occurred")
        raise error


def admin_confirm_sign_up(cognito_cli, user_pool_id, _username):
    """

    :param cognito_cli:
    :param user_pool_id:
    :param _username:
    :return:
    """
    return cognito_cli.admin_confirm_sign_up(
        UserPoolId=user_pool_id, Username=_username
    )


def admin_get_user(cognito_cli, user_pool_id, email):
    """

    :param cognito_cli:
    :param user_pool_id:
    :param email:
    :return:
    """
    return cognito_cli.admin_get_user(
        UserPoolId=user_pool_id,
        Username=email,
    )


def admin_delete_user(cognito_cli, user_pool_id, email):
    """

    :param cognito_cli:
    :param user_pool_id:
    :param email:
    :return:
    """
    return cognito_cli.admin_delete_user(
        UserPoolId=user_pool_id,
        Username=email,
    )


def authenticate_user(cognito_cli, cognito_client_id, email, password):
    try:
        Logger.info("Authenticating user")
        auth_response = cognito_cli.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
            ClientId=cognito_client_id,
        )
        Logger.info(
            {"message": "Successfully authenticated user", "response": auth_response}
        )
        Logger.debug({"message": "User authentication succeeded"})
    except cognito_cli.exceptions.NotAuthorizedException as not_authorized_user:
        raise InvalidCredentials(f"Incorrect username or password")
    except cognito_cli.exceptions.UserNotFoundException as not_found_user:
        raise UserNotFound(f"User does not exist")
    except cognito_cli.exceptions.UserNotConfirmedException as not_confirmed_user:
        raise UserNotConfirmed(f"User is not confirmed")

    id_token = auth_response["AuthenticationResult"]["IdToken"]
    refresh_token = auth_response["AuthenticationResult"]["RefreshToken"]
    token_type = auth_response["AuthenticationResult"]["TokenType"]

    authentication_results = {
        "id_token": id_token,
        "refresh_token": refresh_token,
        "token_type": token_type,
    }
    Logger.debug({"authentication_results": authentication_results})

    Logger.info({"message": "Retrieving user info from idToken"})
    return authentication_results
