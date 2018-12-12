"""This module contains the wrapped functions for the player route
For the documentation on them see the origin file: backend/api/routes/player.py
"""
import logging

from backend.security.validation import user

logger = logging.getLogger(__name__)


#
# PlayerPlayPause
#
@user
def p_p_p_get(username: str):
    """Returns the state of the player.

    Args:
        username: This is just for logging purposes
    """
    pass


@user
def p_p_p_put(state: str, username: str):
    """Sets the state of the player

    Args:
        state: The state which the player should take [play, pause, stop]
        username: This is just for logging purposes
    """
    pass


#
# PlayerNext
#
@user
def p_n_get(username: str):
    """Returns the next song

    Args:
        username: This is just for logging purposes
    """
    pass


@user
def p_n_put(username: str):
    """Plays the next song

    Args:
        username: This is just for logging purposes
    """
    pass


#
# PlayerPrevious
#
@user
def p_p_get(username: str):
    """Returns the previous song

    Args:
        username: This is just for logging purposes
    """
    pass


@user
def p_p_put(username: str):
    """Plays the previous song

    Args:
        username: This is just for logging purposes
    """
    pass


#
# PlayerShuffle
#
@user
def p_s_get(username: str):
    """Returns whether shuffle is on or off

    Args:
        username: This is just for logging purposes
    """
    pass


@user
def p_s_put(username: str):
    """Sets shuffle to the opposite value

    Args:
        username: This is just for logging purposes
    """
    pass


#
# PlayerRepeat
#
@user
def p_r_get(username: str):
    """Returns whether repeat is on or off

    Args:
        username: This is just for logging purposes
    """
    pass


@user
def p_r_put(username: str):
    """Sets repeat to the opposite value

    Args:
        username: This is just for logging purposes
    """
    pass
