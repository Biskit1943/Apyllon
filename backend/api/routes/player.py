import logging

from flask.json import jsonify
from flask.views import MethodView

logger = logging.getLogger(__name__)


class PlayerPlayPause(MethodView):

    def get(self):
        """Returns the state of the player.
        """
        return jsonify("{Message: No!}")

    def put(self, state: str, username: str):
        """Sets the state of the player

        Args:
            state: The state which the player should take [play, pause, stop]
            username: This is just for logging purposes
        """
        return jsonify("{Message: No!}")


class PlayerNext(MethodView):

    def get(self):
        """Returns the next song
        """
        return jsonify("{Message: No!}")

    def put(self, username: str):
        """Plays the next song

        Args:
            username: This is just for logging purposes
        """
        return jsonify("{Message: No!}")


class PlayerPrevious(MethodView):

    def get(self):
        """Returns the previous song
        """
        return jsonify("{Message: No!}")

    def put(self, username: str):
        """Plays the previous song

        Args:
            username: This is just for logging purposes
        """
        return jsonify("{Message: No!}")


class PlayerShuffle(MethodView):

    def get(self):
        """Returns whether shuffle is on or off
        """
        return jsonify("{Message: No!}")

    def put(self, username: str):
        """Sets shuffle to the opposite value

        Args:
            username: This is just for logging purposes
        """
        return jsonify("{Message: No!}")


class PlayerRepeat(MethodView):

    def get(self):
        """Returns whether repeat is on or off
        """
        return jsonify("{Message: No!}")

    def put(self, username: str):
        """Sets repeat to the opposite value

        Args:
            username: This is just for logging purposes
        """
        return jsonify("{Message: No!}")
