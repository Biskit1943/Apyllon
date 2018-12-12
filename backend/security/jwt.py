import logging
import os
from typing import Dict, Tuple

import jwt

from config import Config
from backend.database.exceptions import DoesNotExist
from backend.database.models import User

logger = logging.getLogger(__name__)


def validate_token(token: str) -> Tuple[str, str]:
    """Returns username and password if the token is valid else it will raise
    an error.

    Args:
        token: The JWT as string

    Returns:
        A Tuple with the username and the password

    Raises:
        FileNotFoundError: If the public  key was not found
        ValueError: If the JWT is invalid
        KeyError: If username or password were not in the Key
    """
    if not os.path.exists(Config.PUBLIC_KEY):
        logger.error('Config.PUBLIC_KEY was not found')
        raise FileNotFoundError("Public key was not found")

    with open(Config.PUBLIC_KEY) as key:
        public = key.read()

    try:
        payload = jwt.decode(token, public, algorithms=['RS256'])
        username = payload['username']
        password = payload['password']
    except ValueError as e:
        logger.debug(f'Raising error ==> {e}')
        raise
    except KeyError as e:
        logger.debug(f'Raising error ==> {e}')
        raise
    except Exception as e:
        logger.critical(f'Raising error ==> {e}')
        raise e
    else:
        return username, password


def gen_jwt(password: str, uid: int = None, username: str = None) -> Dict:
    """Generates a jwt with the given username and password and the private key
    which is defined in the config

    NOTE: The user MUST be present in the database

    Args:
        password: The 64 character blake2b hash
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
        FileNotFoundError: If the secret key was not found
        DoesNotExist: If the requested user does not exist
        RuntimeError:
            - If the created JWT fails the validation
            - If the function call didn't contain uid or username
        ValueError: If the password for the user is not correct
    """
    if not os.path.exists(Config.SECRET_KEY):
        raise FileNotFoundError("Secret key was not found")

    if uid:
        user = User.query.filter_by(uid=uid).first()
    elif username:
        user = User.query.filter_by(username=username).first()
    else:
        logger.critical('This function needs to be called with uid OR username(at least one of them)')
        raise RuntimeError("Neither uid nor username was given")

    if user is None:
        raise DoesNotExist(f'User with uid<{username}> was not found')
    elif uid:
        # Make sure the username is set when we received a uid
        username = user.username

    if user.password_hash != password:
        logger.error('Passwords did not match')
        raise ValueError("Passwords did not match")

    with open(Config.SECRET_KEY) as key:
        secret = key.read()

    token = jwt.encode({
        'username': username,
        'password': password
    }, secret, algorithm='RS256')

    try:  # Just make sure we don't fucked the creation up
        validate_token(token)
    except FileNotFoundError as e:
        logger.debug(f'Raising Error ==> {e}')
    except KeyError as e:
        logger.debug(f'Raising Error ==> {e}')
        raise
    except Exception as e:
        logger.critical(f'raising Error ==> {e}')
        raise

    answer = user.to_dict()
    answer['token'] = str(token)

    return answer
