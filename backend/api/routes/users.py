"""Provide the routes for users interaction"""
import logging

from flask import (
    request,
    jsonify)
from flask.views import MethodView

from backend.api.routes import exceptions
from backend.database import user_utils
from backend.database.exceptions import (
    Exists,
    DoesNotExist,
)

logger = logging.getLogger('__main__')


class UsersIdView(MethodView):
    """Provides the HTTP methods for user related things with the user ID as
    identification
    """

    def get(self, uid: int):
        try:
            user = user_utils.get_user(uid=uid)
        except KeyError as e:
            logger.error(f'Error while getting user ==> {e}')
            raise

        if not user:
            logger.warning(f'User <{uid}> not found')
            return f'User <{uid}> not found', 404

        return jsonify(user.to_dict())

    def put(self, uid: int):
        if not request.is_json:
            raise exceptions.BadRequest('Missing user json', {
                'username': 'Biskit1943',
                'password': 'blake2 hash',
            })
        return f'PUT /users/{uid} + json'

    def delete(self, uid: int):
        try:
            user_utils.delete_user(uid=uid)
        except KeyError as e:
            logger.error(f'Error while deleting user ==> {e}')
            raise
        except NameError as e:
            logger.error(f'Error while deleting user ==> {e}')
            return f'User <{uid}> not found', 404

        logger.info(f'Deleted user <{uid}>')
        return f'Deleted user <{uid}>', 200


class UsersNameView(MethodView):
    """Provides the HTTP methods for user related things with the username as
    identification
    """

    def get(self, username: str):
        try:
            user = user_utils.get_user(username=username)
        except KeyError as e:
            logger.error(f'Error while getting user ==> {e}')
            raise

        if not user:
            logger.warning(f'User <{username}> not found')
            return f'User <{username}> not found', 404

        return jsonify(user.to_dict())

    def put(self, username: str):
        if not request.is_json:
            raise exceptions.BadRequest('Missing user json', {
                'username': 'Biskit1943',
                'password': 'blake2 hash',
            })
        return f'PUT /users/{username} + json'

    def delete(self, username: str):
        try:
            user_utils.delete_user(username=username)
        except KeyError as e:
            logger.error(f'Error while deleting user ==> {e}')
            raise
        except NameError as e:
            logger.warning(f'Error while deleting user ==> {e}')
            return f'User <{username}> not found', 404

        logger.info(f'Deleted user <{username}>')
        return f'Deleted user <{username}>', 200


class UserView(MethodView):
    """Provides the HTTP methods for general user related things like
    registration or listing all users
    """

    def get(self):
        return jsonify(user_utils.list_users())

    def post(self):
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


class UsersIdAuthView(MethodView):
    """Provides the HTTP methods for user authentication with the user ID"""

    def post(self, uid: int):
        password = request.form['password']

        try:
            answer = user_utils.auth_user(password=password, uid=uid)
        except DoesNotExist as e:
            logger.warning(f'Error while logging in ==> {e}')
            return str(e), 404

        return jsonify(answer)


class UsersNameAuthView(MethodView):
    """Provides the HTTP methods for user authentication with the username"""

    def post(self, username: str):
        password = request.form['password']

        try:
            answer = user_utils.auth_user(password=password, username=username)
        except DoesNotExist as e:
            logger.warning(f'Error while logging in ==> {e}')
            return str(e), 404

        return jsonify(answer)
