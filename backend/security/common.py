import logging

from backend.database import song_utils
from flask import jsonify

logger = logging.getLogger(__name__)


def list_songs():
    """
    Returns all songs in the database
    """
    try:
        return jsonify(song_utils.list_songs()), 200
    except AssertionError as e:
        logger.error(e)
        return str(e), 404
