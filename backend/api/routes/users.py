"""Provide the routes for users interaction
NOTE: If there is a wrapper needed for the route you have to put the function
      into an extra file with a wrapper around it an call it here. Flasgger
      can't handle @wrapper on routes.
      The functions for this module are in backend/security/users.py
"""
import logging

from flask import request, jsonify
from flask.views import MethodView

from backend.security.users import (
    u_i_v_get,
    u_i_v_put,
    u_i_v_delete,
    u_n_v_get,
    u_n_v_put,
    u_n_v_delete,
    u_v_get,
    u_v_post,
    u_i_a_v_post,
    u_n_a_v_post,
    u_n_c_p_post
)
from backend.database import user_utils
from backend.database.exceptions import DoesNotExist

logger = logging.getLogger(__name__)


class UsersIdView(MethodView):
    """Provides the HTTP methods for user related things with the user ID as
    identification
    """

    def get(self, uid: int):
        """Returns the user with the given id

        Args:
            uid: The id of the requested user

        Returns:
            The user JSON
        """
        return u_i_v_get(uid)

    def put(self, uid: int):
        """Creates a user with the given id

        Args:
            uid: The id which the user should have

        Returns:
            The new user as JSON
        """
        return u_i_v_put(uid)

    def delete(self, uid: int):
        """Deletes the user with a given id

        Args:
            uid: The uid of the user which should be deleted
        """
        return u_i_v_delete(uid)


class UsersNameView(MethodView):
    """Provides the HTTP methods for user related things with the username as
    identification
    """

    def get(self, username: str):
        """Returns the user with the given username

        Args:
            username: The username of the requested user

        Returns:
            The user JSON
        """
        return u_n_v_get(username)

    def put(self, username: str):
        """Creates a user with the given name

        Args:
            username: The name which the user should have

        Returns:
            The new created user as JSON
        """
        return u_n_v_put(username)

    def delete(self, username: str):
        """Deletes the user with the given name

        Args:
            username: The name of the user which should be deleted
        """
        return u_n_v_delete(username)


class UserView(MethodView):
    """Provides the HTTP methods for general user related things like
    registration or listing all users
    """

    def get(self):
        """Returns all users"""
        return u_v_get()

    def post(self):
        """Register a new user"""
        return u_v_post()


class UsersIdAuthView(MethodView):
    """Provides the HTTP methods for user authentication with the user ID"""

    def post(self, uid: int):
        """Checks if the user with the id has a valid login (JWT)

        Args:
            uid: The id of the user which made the request
        """
        return u_i_a_v_post(uid)


class UsersNameAuthView(MethodView):
    """Provides the HTTP methods for user authentication with the username"""

    def post(self, username: str):
        """Checks if the user with the name has a valid login (JWT)

        Args:
            username: The name of the user which made the request
        """
        return u_n_a_v_post(username)


class UsersNameChangePassword(MethodView):

    def post(self, username: str):
        return u_n_c_p_post(username)
