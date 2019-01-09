"""This module contains the wrapped functions for the player route
For the documentation on them see the origin file: backend/api/routes/player.py
"""
import logging

from backend.security.validation import user
from backend.player import player

logger = logging.getLogger(__name__)

player = player.Player()
# TODO:  This is just done for mocking
player.add_youtube("https://www.youtube.com/watch?v=LBZ-3Ugj1AQ")
player.add_youtube("https://www.youtube.com/watch?v=U5u9glfqDsc")


#
# PlayerPlayPause
#
@user
def p_p_p_get():
    """Returns the state of the player"""
    return "GET /play/pause"


@user
def p_p_p_put():
    """Sets the state of the player

    Args:
        state: The state which the player should take [play, pause, stop]
        username: This is just for logging purposes
    """
    # TODO get state and username from body
    state = 'play'
    if state == "play":
        player.play()
    elif state == "pause":
        player.pause()
    elif state == "stop":
        player.stop()

    return f'PUT /player/play_pause{state}'


#
# PlayerNext
#
@user
def p_n_get():
    """Returns the next song"""
    return 'GET /player/next'


@user
def p_n_put():
    """Plays the next song

    Args:
        username: This is just for logging purposes
    """
    player.next()
    return 'PUT /player/next'


#
# PlayerPrevious
#
@user
def p_p_get():
    """Returns the previous song"""
    return 'GET /player/previous'


@user
def p_p_put():
    """Plays the previous song

    Args:
        username: This is just for logging purposes
    """
    player.previous()
    return 'PUT /player/previous'


#
# PlayerShuffle
#
@user
def p_s_get():
    """Returns whether shuffle is on or off"""
    return 'GET /player/shuffle'


@user
def p_s_put():
    """Sets shuffle to the opposite value

    Args:
        username: This is just for logging purposes
    """
    return 'PUT /player/shuffle'


#
# PlayerRepeat
#
@user
def p_r_get():
    """Returns whether repeat is on or off"""
    return 'GET /player/repeat'


@user
def p_r_put():
    """Sets repeat to the opposite value

    Args:
        username: This is just for logging purposes
    """
    player.set_playback_mode("repeat")
    return 'PUT /player/repeat'
