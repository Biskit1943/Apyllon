"""Utility for the user table in the database.
All user related actions which involve the database belong here, except the
ones which deal with security. The security related functions can be found in
`backend/security/user.py`.
"""
import json
import logging
from typing import (
    Dict,
    List,
    Union,
    Tuple,
)

from backend import db
from backend.database.exceptions import (
    Exists,
    DoesNotExist,
)
from backend.database.models import User
from backend.security import jwt

logger = logging.getLogger(__name__)


def add_user(data: Union[Dict, str]) -> Tuple[User, Dict]:
    """Adds a new user to the database

    Args:
        data: A dict or string in JSON schema as defined in
        `backend/templates/swagger/template.yml#definitions/UserRegister`

    Returns:
        A tuple containing the new created User object and a dict containing the
        user information as dict and the generated JWT
        ex.:
        (
            <user at 0x13984>,
            {
                username: str,
                password: str,
                token: str,
            }
        )

    """
    logger.debug(f'add_user({data})')
    if type(data) is str or bytes:
        logger.debug('parsing JSON')
        data = json.loads(data, strict=False)  # strict enables bytes

    try:
        username = data['username']
        password = data['password']
    except KeyError as e:
        logger.error(f'Error while adding user ==> {e}')
        raise

    if len(password) != 128:
        logger.error(f'password length does not match')
        raise ValueError(f'password has {len(password)} characters but must be 128 characters long')

    if len(User.query.filter_by(username=username).all()) > 0:
        logger.error(f'user already exist')
        raise Exists(f'pser with username <{username}> already exist')

    user = User(username=username, password_hash=password)
    # print('users!!!!!!!!!!!!', User.query.all())
    db.session.add(user)
    db.session.commit()

    token = jwt.gen_jwt(password=password, username=username)

    return user, token


def list_users() -> List:
    """Returns a list of users

    Returns:
        A list containing users dicts from the database. See
        `backend/templates#definitions/Users` for a reference
    """
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())

    logger.debug(f'returning {len(users_list)} users')
    return users_list


def get_user(uid: int = None, username: str = None) -> Union[User, None]:
    """Returns the user with the given id or given username

    Args:
        uid: (default=None) The id of the requested user
        username: (default=None) The username of the requested user

    Returns:
        The User object with the given id/username or None if not found

    Raises:
        KeyError: If uid and username was set or none of them
    """
    logger.debug(f'get_user({uid}, {username})')
    try:
        data = _filter_dict(uid=uid, username=username)
    except KeyError as e:
        logger.error(f'Error while getting the data ==> {e}')
        raise

    try:
        user = User.query.filter_by(**data).first()
    except NameError as e:
        logger.warning(f'Error while getting the user ==> {e}')
        return
    else:
        return user


def delete_user(uid: int = None, username: str = None):
    """Deletes a user with the given id or given username

    Args:
        uid: (default=None) The id of the requested user
        username: (default=None) The username of the requested user

    Raises:
        KeyError: If uid and username was set or none of them
    """
    logger.debug(f'delete_user({uid}, {username})')
    try:
        data = _filter_dict(uid=uid, username=username)
    except KeyError as e:
        logger.error(f'Error while getting the data ==> {e}')
        raise

    try:
        user = User.query.filter_by(**data).first()
        db.session.delete(user)
    except NameError as e:
        logger.error(f'Error while getting the user ==> {e}')
        raise


def auth_user(password: str, uid: int = None, username: str = None) -> Dict:
    """Authenticates a user and returns it's token for further validation.
    This will not check the JWT instead it will generate a JWT from a request.

    For validation see the security module.

    Args:
        password: The password of the user (blake2b hashed)
        uid: (default=None) The uid of the user which has to be authenticated
        username: (default=None) The username of the user which has to be
            authenticated

    Returns:
        A dict with the given information plus the JWT token. Ex.:
        {
            username: str,
            password: str,
            token: str,
        }

    Raises:
        KeyError: If uid and username was set or none of them
        FileNotFoundError: If the private key was not found
        RuntimeError: If the created JWT fails the validation
        ValueError: If the password for the user is not correct
    """
    logger.debug(f'auth_user({password}, {uid}, {username})')
    try:
        data = _filter_dict(uid=uid, username=username)
    except KeyError as e:
        logger.error(f'Error while getting the data ==> {e}')
        raise

    if not get_user(**data):
        logger.error(f'The user <{data}> does not exit')
        raise DoesNotExist(f'The user <{data}> does not exit')

    try:
        answer = jwt.gen_jwt(password, **data)
    except FileNotFoundError:
        raise
    except RuntimeError:
        raise
    except ValueError:
        raise
    else:
        return answer


def change_password(password: str, uid: int = None, username: str = None):
    """Changes the password of the given user

    Args:
        password: The new password
        uid: The id of the user who want to change the PW (Do not user both uid
            and username)
        username: The name fo the user who want to change the PW (Do not user
            both uid and username)

    Raises:
        KeyError: When both uid and username were given
        DoesNotExist: When the user does not exist
        ValueError: If the Password does not meet the Blake2b length
    """
    try:
        data = _filter_dict(uid=uid, username=username)
    except KeyError as e:
        logger.debug(f'Error while getting the data ==> {e}')
        raise

    user = get_user(**data)
    if not user:
        logger.error(f'The user <{data}> does not exit')
        raise DoesNotExist(f'The user <{data}> does not exit')

    if len(password) != 128:
        logger.error(f'password length does not match')
        raise ValueError(f'password has {len(password)} characters but must be 128 characters long')

    user.password_hash = password
    if not user.password:
        user.password = True
    db.session.commit()
    logger.info("Changed password of admin")


def _filter_dict(**kwargs) -> Dict:
    """Returns a dict with only one value from kwargs which was not None

    Args:
        **kwargs: A dict with key: value attributes where exact one should be
            not None

    Returns:
        A dict with the one key which was not none
        ex.:
            <= { 'uid': None, 'username': 'Biskit1943' }
            => { 'username': 'Biskit1943' }

    Raises:
        KeyError: If either more than one value was set or zero values were set
    """
    logger.debug(f'_filter_dict({kwargs})')
    data = {}
    for key, value in kwargs.items():
        if value:
            data[key] = value

    if len(data) > 1:
        logger.debug(f'len(data) == {len(data)}')
        raise KeyError('More than one value was not None')
    elif len(data) == 0:
        logger.debug(f'len(data) == {len(data)}')
        raise KeyError('No value was given')
    else:
        return data
