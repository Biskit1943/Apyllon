"""Utility for the user table in the database.
All user related actions which involve the database belong here, except the
ones which deal with security. The security related functions can be found in
`backend/security/user.py`.
"""
import json
import logging
import sys

logger = logging.getLogger('__main__')

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
from backend.security import user as user_sec


def add_user(data: Union[Dict, str]) -> Tuple[User, Dict]:
    """Adds a new user to the database

    Args:
        data: A dict or string in JSON schema as defined in
        `backend/templates/swagger/template.yml#definitions/UserRegister`

    Returns:
        A tuple containing the new created User object and a dict containing the
        user information with the generated JWT
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

    if len(password) != 88:  # Blake2b.hexdigest() -> 128 chars
        logger.error(f'password length does not match')
        raise ValueError(f'password has {len(password)} characters but must be 128 characters long')

    if len(User.query.filter_by(username=username).all()) > 0:
        logger.error(f'user already exist')
        raise Exists(f'pser with username <{username}> already exist')

    user = User(username=username, password_hash=password)
    db.session.add(user)
    db.session.commit()

    token = user_sec.gen_jwt(password=password, username=username)

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
    """Authenticates a user and returns it's token for further validation

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
        answer = user_sec.gen_jwt(password, **data)
    except FileNotFoundError:
        raise
    except RuntimeError:
        raise
    except ValueError:
        raise
    else:
        return answer


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
