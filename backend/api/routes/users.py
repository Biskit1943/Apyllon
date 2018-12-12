"""Provide the routes for users interaction"""
import logging

from flask import (
    request,
    jsonify
)
from flask.views import MethodView

from backend.api.routes import exceptions
from backend.database import user_utils
from backend.database.exceptions import (
    Exists,
    DoesNotExist,
)
from backend.security.validation import (
    admin,
    validate_admin
)

logger = logging.getLogger(__name__)


class UsersIdView(MethodView):
    """Provides the HTTP methods for user related things with the user ID as
    identification
    """

    @validate_admin
    @admin
    def get(self, uid: int):
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
    def put(self, uid: int):
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
    def delete(self, uid: int):
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


class UsersNameView(MethodView):
    """Provides the HTTP methods for user related things with the username as
    identification
    """

    @validate_admin
    @admin
    def get(self, username: str):
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
    def put(self, username: str):
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
    def delete(self, username: str):
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


class UserView(MethodView):
    """Provides the HTTP methods for general user related things like
    registration or listing all users
    """

    @validate_admin
    @admin
    def get(self):
        """Returns all users"""
        return jsonify(user_utils.list_users())

    @validate_admin  # Only allow registration if the admin login was changed
    def post(self):
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


class UsersIdAuthView(MethodView):
    """Provides the HTTP methods for user authentication with the user ID"""

    def post(self, uid: int):
        """Checks if the user with the id has a valid login (JWT)

        Args:
            uid: The id of the user which made the request
        """
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
        """Checks if the user with the name has a valid login (JWT)

        Args:
            username: The name of the user which made the request
        """
        password = request.form['password']

        try:
            answer = user_utils.auth_user(password=password, username=username)
        except DoesNotExist as e:
            logger.warning(f'Error while logging in ==> {e}')
            return str(e), 404

        return jsonify(answer)
