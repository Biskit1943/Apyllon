"""Provide the routes for common interactions
NOTE: If there is a wrapper needed for the route you have to put the function
      into an extra file with a wrapper around it an call it here. Flasgger
      can't handle @wrapper on routes.
      The functions for this module are in backend/security/common.py
"""
import logging

from flask.views import MethodView

from backend.security.common import list_songs
from backend.security.update import update
from backend.security.upload import u_post

logger = logging.getLogger(__name__)


class ListSongsView(MethodView):
    """Provides Methods to return Songs from the database"""

    def get(self):
        """Returns a List of all Songs in the database, if there are any."""
        return list_songs()


class UploadView(MethodView):

    def post(self):
        return u_post()


class UpdateView(MethodView):

    def put(self):
        return update()
