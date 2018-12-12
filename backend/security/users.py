"""This file fixes the errors Flasgger has with annotations as this serves
as a second wrapper around the called route itself

For the documentation of the functions see the File where they are called:
backend/api/routes/users.py
"""
import logging

from flask import (
    request,
    jsonify
)

from backend.api.routes import exceptions
from backend.database import user_utils
from backend.database.exceptions import Exists
from backend.security.validation import (
    admin,
    validate_admin,
)

logger = logging.getLogger(__name__)


#
# UsersIdView
#
@validate_admin
@admin
def u_i_v_get(uid: int):
    """Returns the user with the given id

    Args:
        uid: The id of the requested user

    Returns:
        The user JSON
    """
    try:
        user = user_utils.get_user(uid=uid)
    except KeyError as e:
        logger.debug(f'Raising error ==> {e}')
        raise

    if not user:
        logger.warning(f'User <{uid}> not found')
        return f'User <{uid}> not found', 404

    return jsonify(user.to_dict())


@validate_admin
@admin
def u_i_v_put(uid: int):
    """Creates a user with the given id

    Args:
        uid: The id which the user should have

    Returns:
        The new user as JSON
    """
    if not request.is_json:
        logger.error("Missing user JSON or JSON not valid")
        raise exceptions.BadRequest('Missing user JSON', {
            'username': 'Biskit1943',
            'password': 'blake2 hash',
        })
    return f'PUT /users/{uid} + json'


@validate_admin
@admin
def u_i_v_delete(uid: int):
    """Deletes the user with a given id

    Args:
        uid: The uid of the user which should be deleted
    """
    try:
        user_utils.delete_user(uid=uid)
    except KeyError as e:
        logger.debug(f'Raising error ==> {e}')
        raise
    except NameError as e:
        logger.debug(f'Raising error ==> {e}')
        return f'User <{uid}> not found', 404

    logger.info(f'Deleted user <{uid}>')
    return f'Deleted user <{uid}>', 200


#
# UsersNameView
#
@validate_admin
@admin
def u_n_v_get(username: str):
    """Returns the user with the given username

    Args:
        username: The username of the requested user

    Returns:
        The user JSON
    """
    try:
        user = user_utils.get_user(username=username)
    except KeyError as e:
        logger.debug(f'Raising error ==> {e}')
        raise

    if not user:
        logger.warning(f'User <{username}> not found')
        return f'User <{username}> not found', 404

    return jsonify(user.to_dict())


@validate_admin
@admin
def u_n_v_put(username: str):
    """Creates a user with the given name

    Args:
        username: The name which the user should have

    Returns:
        The new created user as JSON
    """
    if not request.is_json:
        logger.error("Missing user JSON or JSON not valid")
        raise exceptions.BadRequest('Missing user JSON', {
            'username': 'Biskit1943',
            'password': 'blake2 hash',
        })
    return f'PUT /users/{username} + json'


@validate_admin
@admin
def u_n_v_delete(username: str):
    """Deletes the user with the given name

    Args:
        username: The name of the user which should be deleted
    """
    try:
        user_utils.delete_user(username=username)
    except KeyError as e:
        logger.debug(f'Raising error ==> {e}')
        raise
    except NameError as e:
        logger.warning(f'Error while deleting user ==> {e}')
        return f'User <{username}> not found', 404

    logger.info(f'Deleted user <{username}>')
    return f'Deleted user <{username}>', 200


#
# UserView
#
@validate_admin
@admin
def u_v_get():
    """Returns all users"""
    return jsonify(user_utils.list_users())


@validate_admin  # Only allow registration if the admin login was changed
def u_v_post():
    """Register a new user"""
    if not request.is_json:
        logger.error('The request needs a valid JSON')
        raise exceptions.BadRequest('Missing user json', {
            'username': 'Biskit1943',
            'password': 'blake2 hash',
        })

    try:
        _, answer = user_utils.add_user(request.data)
    except Exists as e:
        logger.error(f'Error while creating user ==> {e}')
        raise exceptions.Conflict(str(e))
    return jsonify(answer)