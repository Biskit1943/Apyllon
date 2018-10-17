"""This module provides utilities for the song table in the database"""
import sys

from app import db
from app.database.models import Song


def add_songs(song: dict):
    """Adds (a) song(s) to the database

    Args:
        song: A dict in JSON schema as defined in `app/templates/scan.json`,
        containing one song.

    Raises:
        AssertionError: When the type of the casted YAML string is not dict
        KeyError: When the YAML string is missing a value
    """
    try:
        filename = song['filename']
        path = song['path']
        length = int(song['length'])

        meta_data = song['meta']
        artist = meta_data['artist']
        title = meta_data['title']
        genre = meta_data['genre']

    except KeyError as e:
        print(e, file=sys.stderr)
        raise
    else:
        song = Song(filename=filename, directory=path, artist=artist, title=title, genre=genre, length=length)

        print(f'Adding {song} to database')
        db.session.add(song)
        db.session.commit()
