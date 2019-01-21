"""This file contains all security related wrapper functions for the routes."""
import logging
from typing import Callable
from functools import wraps

from flask import request

from backend.security.jwt import validate_token
from backend.database.models import User

logger = logging.getLogger(__name__)


class Login:
    """This class will hold the information if the admin login was changed by
    the user. This was made to prevent the program from constantly checking the
    DB and needs to be refreshed on restart.
    """

    def __init__(self):
        self.admin = False


login = Login()


def validate_admin(func: Callable):
    """This wrapper makes sure the admin password was set by a user, append this
    to all routes which are not the admin login or admin password change and
    which require admin access. On user access this function is already in the
    @user decorator.

    Args:
        func: The function which will be wrapped

    Returns:
        The origin function or the HTTP answer if the admin wasn't verified
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        if login.admin:
            return func(*args, **kwargs)

        u = User.query.filter_by(uid=1).first()
        if u:
            if not u.password:
                logger.warning("Admin password is still default!")
                return "Admin password is still default!", 401
            else:
                logger.debug("Admin password was changed setting login to true")
                login.admin = True
                return func(*args, **kwargs)
        else:
            return "Admin account does not exist", 500

    return wrap


def user(func: Callable):
    """This wrapper will validate the JWT. On failure it will automatically
    return the corresponding message and error-code for the API.

    Args:
        func: The function which will be wrapped

    Returns:
        Either the wrapped function or the answer for the request if the
        validation failed.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        if not login.admin:
            return 'Password is still default!', 401

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

    return wrap


def admin(func: Callable):
    """This wrapper will validate the JWT. On failure it will automatically
    return the corresponding message and error-code for the API.
    The special thing about this is, it will check if the user has admin
    privileges.

    Args:
        func: The function which will be wrapped

    Returns:
        Either the wrapped function or the answer for the request if the
        validation failed.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
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

    return wrap
