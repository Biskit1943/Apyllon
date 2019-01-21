import os

from config import Config
from backend.database import song_utils
from backend.database.exceptions import Exists
from backend.search import file_search


def update():
    path = Config.HOME
    if not os.path.exists(path):
        raise LookupError("Directory does not exist")

    crawler = file_search.FileSearch()
    songs = crawler.search(path, *Config.REQUIRED_META_DATA)
    for song in songs:
        try:
            song_utils.add_song(song)
        except Exists:
            # TODO check if data changed
            pass

    return 'Success', 200
