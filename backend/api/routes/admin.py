"""Provide the routes for users interaction"""
import logging

from flask.views import MethodView
from backend.security.validation import admin

logger = logging.getLogger(__name__)


class Default(MethodView):
    """Provides the HTTP methods for user related things with the user ID as
    identification
    """

    @admin
    def get(self):
        """This route is only available when the admin hasn't change his
        password yet.
        This route will return 200 if the admin was logged in successfully.
        After that he has to change the password before he can do anything.
        """
        return "Nope"

    @admin
    def put(self, password: str):
        """This route is for changing the PW of the admin"""
        return "Nope"
