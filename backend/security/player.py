"""This module contains the wrapped functions for the player route
For the documentation on them see the origin file: backend/api/routes/player.py
"""
import logging
from flask import request, jsonify

from backend.security.validation import user
from backend.player.player import Player
from backend.database.song_utils import get_song
from backend.database.exceptions import DoesNotExist
from backend.player.exceptions import NotFound

logger = logging.getLogger(__name__)

player = Player()
# TODO:  This is just done for mocking
player.add_youtube("https://www.youtube.com/watch?v=LBZ-3Ugj1AQ")
player.add_youtube("https://www.youtube.com/watch?v=U5u9glfqDsc")


#
# PlayerPlayPause
#

def p_p_p_get():
    """Returns the state of the player"""
    return "GET /play/pause"


def p_p_p_put():
    """Sets the state of the player

    Args:
        state: The state which the player should take [play, pause, stop]
        username: This is just for logging purposes
    """
    req = request.get_json(force=True)
    try:
        username = req['username']
        state = req['state']
    except ValueError as e:
        logger.error(f'missing parameters in body: {req}')
        return str(e), 400
    logger.info(f'User {username} changed state of Player to {state}.')
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

def p_n_get():
    """Returns the next song"""
    return 'GET /player/next'


def p_n_put():
    """Plays the next song

    Args:
        username: This is just for logging purposes
    """
    req = request.get_json(force=True)
    try:
        username = req['username']
    except ValueError as e:
        return str(e), 400
    logger.info(f'User {username} requested to play the next song')
    player.next()
    return 'PUT /player/next'


#
# PlayerPrevious
#
def p_p_get():
    """Returns the previous song"""
    return 'GET /player/previous'


def p_p_put():
    """Plays the previous song

    Args:
        username: This is just for logging purposes
    """
    req = request.get_json(force=True)
    try:
        username = req['username']
    except ValueError as e:
        return str(e), 400
    logger.info(f'User {username} requested to play the previous song')
    player.previous()
    return 'PUT /player/previous'


#
# PlayerShuffle
#
def p_s_get():
    """Returns whether shuffle is on or off"""
    return 'GET /player/shuffle'


def p_s_put():
    """Sets shuffle to the opposite value

    Args:
        username: This is just for logging purposes
    """
    req = request.get_json(force=True)
    try:
        username = req['username']
    except ValueError as e:
        return str(e), 400
    logger.info(f'User {username} requested to change the shuffle state')
    return 'PUT /player/shuffle'


#
# PlayerRepeat
#
def p_r_get():
    """Returns whether repeat is on or off"""
    state = player.get_playback_mode()
    return state, 200


def p_r_put():
    """Sets repeat to the opposite value

    Args:
        username: This is just for logging purposes
    """
    req = request.get_json(force=True)
    try:
        username = req['username']
    except ValueError as e:
        return str(e), 400
    logger.info(f'User {username} requested to change the repeat state')
    state = 'default' if player.get_playback_mode() != 'default' else 'loop'
    player.set_playback_mode(state)
    return 'PUT /player/repeat'


#
# PlayerPlaylist
#
@user
def p_pl_get():
    """Returns a list with """
    playlist = player.get_playlist_meta()
    return jsonify(playlist), 200


@user
def p_pl_put():
    req = request.get_json(force=True)
    try:
        username = req['username']
        type_ = req['type']
        path = req['path']
    except ValueError as e:
        logger.error(f'missing parameters in body: {req}')
        return str(e), 400

    if type_ == "file":
        try:
            song = get_song(path)
        except DoesNotExist as e:
            logger.debug(f'[raise] {e}')
            return str(e), 404
        playlist = player.add_local_databse_object(song)

    elif type == "youtube":
        playlist = player.add_youtube(path)

    else:
        logger.error(f'type {type_} unknown')
        return f'type {type_} is not a valid type for a playable item', 400

    logger.info(f'Playlist changed by {username}. Added type: {type_} with path: {path}')
    return jsonify(playlist), 200


@user
def p_pl_delete(index: int, title: str):
    try:
        song = player.remove_from_playlist(index, title)
    except NotFound as e:
        return str(e), 404

    return jsonify(song)
