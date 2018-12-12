"""This file contains all security related wrapper functions for the routes."""
import logging
from typing import Callable

from decorator import decorator
from flask import request

from backend.database.models import User
from backend.security.jwt import validate_token

logger = logging.getLogger(__name__)


class Login:
    """This class will hold the information if the admin login was changed by
    the user. This was made to prevent the program from constantly checking the
    DB and needs to be refreshed on restart.
    """

    def __init__(self):
        self.admin = False


login = Login()


@decorator
def validate_admin(func: Callable, *args, **kwargs):
    """This wrapper makes sure the admin password was set by a user, append this
    to all routes which are not the admin login or admin password change and
    which require admin access. On user access this function is already in the
    @user decorator.

    Args:
        func: The function which will be wrapped
        args: The args of the origin function
        kwargs: The kwargs of the origin function

    Returns:
        The origin function or the HTTP answer if the admin wasn't verified
    """
    if login.admin:
        return func(*args, **kwargs)

    # u = User.query.filter_by(uid=1).first()
    # if u:
    #     if not u.password:
    #         return "Admin password is still default!", 401
    #     else:
    #         login.admin = True
    #         return func(*args, **kwargs)
    # else:
    #     return "Admin account does not exist", 500


@validate_admin
@decorator
def user(func: Callable, *args, **kwargs):
    """This wrapper will validate the JWT. On failure it will automatically
    return the corresponding message and error-code for the API.

    Args:
        func: The function which will be wrapped
        args: The args of the origin function
        kwargs: The kwargs of the origin function

    Returns:
        Either the wrapped function or the answer for the request if the
        validation failed.
    """
    token = str(request.headers['Authorization'])
    try:
        validate_token(token)
    except FileNotFoundError:
        logger.warning('Public key not found')
        return "Public key for decryption not found", 500
    except ValueError:
        logger.warning('JWT invalid')
        return "JWT invalid", 401
    except KeyError:
        logger.warning('JWT corrupt')
        return "JWT corrupt", 400
    except Exception as e:
        return str(e), 500

    return func(*args, **kwargs)


@decorator
def admin(func: Callable, *args, **kwargs):
    """This wrapper will validate the JWT. On failure it will automatically
    return the corresponding message and error-code for the API.
    The special thing about this is, it will check if the user has admin
    privileges.

    Args:
        func: The function which will be wrapped
        args: The args of the origin function
        kwargs: The kwargs of the origin function

    Returns:
        Either the wrapped function or the answer for the request if the
        validation failed.
    """
    token = str(request.headers['Authorization'])
    try:
        username, _ = validate_token(token)
        if username != "admin":
            return "You must be admin to do this!", 401
        # TODO check if uid == 1 and username == admin
    except FileNotFoundError:
        logger.warning('Public key not found')
        return "Public key for decryption not found", 500
    except ValueError:
        logger.warning('JWT invalid')
        return "JWT invalid", 401
    except KeyError:
        logger.warning('JWT corrupt')
        return "JWT corrupt", 400
    except Exception as e:
        return str(e), 500

    return func(*args, **kwargs)