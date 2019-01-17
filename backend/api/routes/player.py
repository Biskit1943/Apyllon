import logging

from flask.views import MethodView

from backend.security.player import (
    p_p_p_get,
    p_p_p_put,
    p_n_get,
    p_n_put,
    p_p_get,
    p_p_put,
    p_s_get,
    p_s_put,
    p_r_get,
    p_r_put,
    p_pl_get,
    p_pl_put,
    p_pl_delete,
)

logger = logging.getLogger(__name__)


class PlayerPlayPause(MethodView):

    def get(self):
        """Returns the state of the player"""
        return p_p_p_get()

    def put(self):
        """Sets the state of the player"""
        return p_p_p_put()


class PlayerNext(MethodView):

    def get(self):
        """Returns the next song"""
        return p_n_get()

    def put(self):
        """Plays the next song"""

        return p_n_put()


class PlayerPrevious(MethodView):

    def get(self):
        """Returns the previous song"""
        return p_p_get()

    def put(self):
        """Plays the previous song"""
        return p_p_put()


class PlayerShuffle(MethodView):

    def get(self):
        """Returns whether shuffle is on or off"""
        return p_s_get()

    def put(self):
        """Sets shuffle to the opposite value"""
        return p_s_put()


class PlayerLoop(MethodView):

    def get(self):
        """Returns whether repeat is on or off"""
        return p_r_get()

    def put(self):
        """Sets repeat to the opposite value"""
        return p_r_put()


class PlayerPlaylist(MethodView):

    def get(self):
        """Returns the playlist with all songs and the user who added each
        of them
        """
        return p_pl_get()

    def put(self):
        """Adds a new song to the playlist. This can be local or a stream"""
        return p_pl_put()

    def delete(self):
        """Removes an item from the playlist"""
        return p_pl_delete()
