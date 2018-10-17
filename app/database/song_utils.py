"""This module provides utilities for the song table in the database"""
import sys

from flask import jsonify

from app import db
from app.database.exceptions import Exists
from app.database.filepath_utils import is_unique
from app.database.models import (
    Song,
    Filepath,
)


def add_songs(song_dict: dict):
    """Adds (a) song(s) to the database

    Args:
        song_dict: A dict in JSON schema as defined in
        `app/templates/scan.json`, containing one song.

    Raises:
        AssertionError: When the type of the casted YAML string is not dict
        KeyError: When the YAML string is missing a value
    """
    try:
        filename = song_dict['filename']
        path = song_dict['path']
        length = int(song_dict['length'])

        meta_data = song_dict['meta']
        artist = meta_data['artist']
        title = meta_data['title']
        album = meta_data['album']
        genre = meta_data['genre']

    except KeyError as e:
        print(e, file=sys.stderr)
        raise
    else:
        if not is_unique(filename, path):
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

        print(f'Adding {song} to database')
        db.session.add(filepath)
        db.session.add(song)
        db.session.commit()


def get_songs() -> str:
    """List all songs from the database"""
    songs = Song.query.all()
    songs_dict = {}
    for song in songs:
        print(f'Adding {song} to dict')
        songs_dict[song.id] = song.to_dict()

    return jsonify(songs_dict)
