import vlc
import pafy
import json

class Queue():
    def __init__(self, identifier):
        self.identifier = identifier
        self.media_list = vlc.MediaList()

    def add_local(self, filepath):
        self.media_list.add_media(filepath)

    def add_local_database_object(self, database_object):
        try:
            media = vlc.Media(database_object.filepath)
            meta = vlc.Meta()
            try:
                meta.Artist = database_object.artist
                meta.Title = database_object.title
                meta.Album = database_object.album
                meta.Genre = database_object.genre
            except(Exception):
                pass
            self.media_list.add_media(media)
        except(Exception):
            pass

    def add_youtube(self, url):
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        self.media_list.add_media(bestaudio.url)

