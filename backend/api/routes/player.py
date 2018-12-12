import logging

from flask.views import MethodView

from backend.security.validation import user

logger = logging.getLogger(__name__)


class PlayerPlayPause(MethodView):

    @user
    def get(self, username: str):
        """Returns the state of the player.

        Args:
            username: This is just for logging purposes
        """
        return "No!"

    @user
    def put(self, state: str, username: str):
        """Sets the state of the player

        Args:
            state: The state which the player should take [play, pause, stop]
            username: This is just for logging purposes
        """
        return "No!"


class PlayerNext(MethodView):

    @user
    def get(self, username: str):
        """Returns the next song

        Args:
            username: This is just for logging purposes
        """
        return "No!"

    @user
    def put(self, username: str):
        """Plays the next song

        Args:
            username: This is just for logging purposes
        """
        return "No!"


class PlayerPrevious(MethodView):

    @user
    def get(self, username: str):
        """Returns the previous song

        Args:
            username: This is just for logging purposes
        """
        return "No!"

    @user
    def put(self, username: str):
        """Plays the previous song

        Args:
            username: This is just for logging purposes
        """
        return "No!"


class PlayerShuffle(MethodView):

    @user
    def get(self, username: str):
        """Returns whether shuffle is on or off

        Args:
            username: This is just for logging purposes
        """
        return "No!"

    @user
    def put(self, username: str):
        """Sets shuffle to the opposite value

        Args:
            username: This is just for logging purposes
        """
        return "No!"


class PlayerRepeat(MethodView):

    @user
    def get(self, username: str):
        """Returns whether repeat is on or off

        Args:
            username: This is just for logging purposes
        """
        return "No!"

    @user
    def put(self, username: str):
        """Sets repeat to the opposite value

        Args:
            username: This is just for logging purposes
        """
        return "No!"
