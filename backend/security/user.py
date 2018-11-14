"""This module provides the functionality for any security related actions in
combination with a user
"""
import logging
import os

import jwt

logger = logging.getLogger('__main__')

from typing import Dict

from config import Config
from backend.database.models import User


def gen_jwt(password: str, uid: int = None, username: str = None) -> Dict:
    """Generates a jwt with the given username and password and the private key
    which is defined in the config

    NOTE: The user MUST be present in the database

    Args:
        password: The 128 character blake2b hash
        uid: The uid of the user for which the jwt is
        username: The username of the user for which the jwt is

    Returns:
        A dict representing the user and the JWT('token').
        The JWT is a BASE64 encoded string with the following payload:
        {
            username: "Biskit1943",
            password: "5bb55...faac2"
        }

    Raises:
        FileNotFoundxists(Config.SECRET_KEY):
        raise FileNotFoundError("Secret key was not found")
Error: If the private key was not found
        RuntimeError:
            - If the created JWT fails the validation
            - If the function call didn't contain uid or username
        ValueError: If the password for the user is not correct
    """
    logger.debug(f'gen_jwt({password}, {uid}, {username})')
    if not os.path.exists(Config.SECRET_KEY):
        raise FileNotFoundError("Secret key was not found")

    if uid:
        user = User.query.filter_by(uid=uid).first()
    elif username:
        user = User.query.filter_by(username=username).first()
    else:
        logger.critical('This function needs to be called with uid OR username(at least one of them)')
        raise RuntimeError("Neither uid nor username was given")

    if user.password_hash != password:
        logger.error('Passwords did not match')
        raise ValueError("Passwords did not match")

    with open(Config.SECRET_KEY) as key:
        secret = key.read()

    token = jwt.encode({
        'username': username,
        'password': password
    }, secret, algorithm='RS256')
    if not validate_token(token):
        logger.critical('Failed to validate token')
        raise RuntimeError('Failed to verify created JWT')

    answer = user.to_dict()
    answer['token'] = str(token)

    return answer


def validate_token(token: str) -> bool:
    """Returns if a given token is valid

    Args:
        token: The JWT as string

    Returns:
        True if the token is valid and False if not

    Raises:
        FileNotFoundError: If the public  key was not found
    """
    logger.debug(f'validate_token({token})')
    if not os.path.exists(Config.PUBLIC_KEY):
        logger.error('Config.PUBLIC_KEY was not found')
        raise FileNotFoundError("Public key was not found")

    with open(Config.PUBLIC_KEY) as key:
        public = key.read()

    try:
        payload = jwt.decode(token, public, algorithms=['RS256'])
        username = payload['username']
        password = payload['password']
    except ValueError:
        logger.debug('validate_token({token}) ==> ValueError ==> return False')
        return False
    except KeyError:
        logger.debug('validate_token({token}) ==> KeyError ==> return False')
        return False
    except Exception as e:
        logger.critical(f'raising Error ==> {e}')
        raise e
    else:
        return True
