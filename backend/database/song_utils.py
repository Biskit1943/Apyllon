"""This module provides utilities for the song table in the database"""
import logging
from typing import Dict

from backend import db
from backend.database.exceptions import (
    Exists,
    DoesNotExist,
)
from backend.database.filepath_utils import (
    is_unique,
    get_filepath,
)
from backend.database.models import (
    Song,
    Filepath,
)

logger = logging.getLogger(__name__)


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


def list_songs() -> list:
    """Returns a list containing all songs

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
    assert len(songs_list) > 0, 'No songs in database'

    return songs_list


def get_song(path: str) -> Song:
    """Returns a song object from the database with the given path

    Args:
        path: The path to the song

    Returns:
        The corresponding song obejct
    """
    try:
        filepath = get_filepath(path)
    except DoesNotExist as e:
        logger.debug(f'[raise] {e}')
        raise
    song = Song.query.filter(Song.filepath is filepath).first()
    if not song:
        logger.error(f'Filepath was found but not the corresponding song: {path}')
        raise DoesNotExist(f'No such song with path {path}')
    return song
