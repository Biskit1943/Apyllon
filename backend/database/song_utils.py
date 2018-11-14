"""This module provides utilities for the song table in the database"""
import logging
import sys

logger = logging.getLogger('__main__')

from typing import Dict

from backend import db
from backend.database.exceptions import Exists
from backend.database.filepath_utils import is_unique
from backend.database.models import (
    Song,
    Filepath,
)


def add_song(data: Dict):
    """Adds a song to the database

    Args:
        data: A dict in JSON schema as defined in
        `backend/templates/swagger/template.yml#definitions/Song`

    Raises:
        AssertionError: When the type of the casted YAML string is not dict
        KeyError: When the YAML string is missing a value
    """
    logger.debug(f'add_song({data}')
    try:
        filename = data['filename']
        path = data['path']
        length = int(data['length'])

        meta_data = data['meta']
        artist = meta_data['artist']
        title = meta_data['title']
        album = meta_data['album']
        genre = meta_data['genre']

    except KeyError as e:
        logger.critical(f'Error while getting object data ==> {e}')
        raise

    if not is_unique(filename, path):
        logger.error(f'{filename} in {path} does already exist')
        raise Exists(f'{filename} in {path} does already exist')

    filepath = Filepath(filename=filename, directory=path)
    song = Song(
        filepath=filepath,
        artist=artist,
        title=title,
        album=album,
        genre=genre,
        length=length
    )

    db.session.add(filepath)
    db.session.add(song)
    db.session.commit()
    logger.debug(f'added {filepath} to database')
    logger.debug(f'added {song} to database')


def list_songs() -> Dict:
    """Returns a list containing of all songs

    Returns:
        A list containing song dicts from the database. See
        `backend/templates#definitions/Songs` for a reference
    """
    logger.debug('list_songs()')
    songs = Song.query.all()
    songs_list = []
    for song in songs:
        songs_list.append(song.to_dict())

    logger.debug(f'returning a list with len = {len(songs_list)}')
    return songs_list
