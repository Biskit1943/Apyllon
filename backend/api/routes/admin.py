"""Provide the routes for users interaction
NOTE: If there is a wrapper needed for the route you have to put the function
      into an extra file with a wrapper around it an call it here. Flasgger
      can't handle @wrapper on routes.
      The functions for this module are in backend/security/admin.py
"""
import logging

from flask.views import MethodView

from backend.security import admin

logger = logging.getLogger(__name__)


class Default(MethodView):
    """Provides methods for changing the password of the admin. This are the
    only routes available if the admin didn't changed the password yet. If he
    did, this routes are gone.
    """

    # @admin
    def get(self):
        """This route is only available when the admin hasn't change his
        password yet.
        This route will return 200 if the admin was logged in successfully.
        After that he has to change the password before he can do anything.
        """
        return admin.get()

    # @admin
    def put(self, password: str):
        """This route is for changing the PW of the admin"""
        return admin.put()
