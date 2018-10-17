"""This Module contains the functions for the local filesystem"""
import os

from app.database import song_utils
from app.database.exceptions import Exists
from app.search import file_search
from config import Config


def add_songs(path: str):
    if not os.path.exists(path):
        raise LookupError("Directory does not exist")

    crawler = file_search.FileSearch()
    songs = crawler.search(path, *Config.REQUIRED_META_DATA)
    for song in songs:
        try:
            song_utils.add_songs(song)
        except Exists:
            # TODO check if data changed
            pass
