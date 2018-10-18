import json
import sys
from typing import (
    Dict,
    List,
    Union,
)

from backend import db
from backend.database.exceptions import (
    Exists,
)
from backend.database.models import User


def add_user(data: Union[Dict, str]) -> User:
    """Adds a new user to the database

    Args:
        data: A dict or string in JSON schema as defined in
        `backend/templates/swagger/template.yml#definitions/UserRegister`

    Returns:
        The new created User object
    """
    if type(data) is str or bytes:
        data = json.loads(data, strict=False)  # strict enables bytes

    try:
        username = data['username']
        password = data['password']
    except KeyError as e:
        print(e, file=sys.stderr)
        raise

    if len(password) != 128:  # Blake2b.hexdigest() -> 128 chars
        raise ValueError(f"Password has {len(password)} characters but must be 128 characters long")

    if len(User.query.filter_by(username=username).all()) > 0:
        raise Exists(f'User with username <{username}> already exist')

    user = User(username=username, password_hash=password)
    db.session.add(user)
    db.session.commit()

    return user


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
    try:
        data = _filter_dict(uid=uid, username=username)
    except KeyError:
        raise

    try:
        user = User.query.filter_by(**data).first()
    except NameError:
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
    try:
        data = _filter_dict(uid=uid, username=username)
    except KeyError:
        raise

    try:
        user = User.query.filter_by(**data).first()
        db.session.delete(user)
    except NameError:
        raise


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
    data = {}
    for key, value in kwargs.items():
        if value:
            data[key] = value

    if len(data) > 1:
        raise KeyError('More than one value was not None')
    elif len(data) == 0:
        raise KeyError('No value was given')
    else:
        return data
