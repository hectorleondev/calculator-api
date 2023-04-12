"""exceptions module"""


class BadRequestException(Exception):
    """
    Bad request exception
    """


class NotFoundException(Exception):
    """
    Not Found  exception
    """


class UserNotFound(Exception):
    """
    User not found
    """


class InvalidCredentials(Exception):
    """
    User not found
    """


class UserNotConfirmed(Exception):
    """
    User not found
    """