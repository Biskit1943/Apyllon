import pafy
import json

class Queue():
    def __init__(self, identifier):
        self.identifier = identifier
        self.songList = []
        self.position = -1
        self.repeat_queue = False
        self.repeat_song = False
        self.shuffle = False

    def get_lenght(self):
        return len(self.songList)

    def add_local(self, filepath):
        mrl = filepath
        meta = Meta()
        self.songList.append(Song(mrl, meta))
        return self.toJson()

    def add_local_database_object(self, database_object):
        mrl, meta = self.database_object_to_mrl_and_meta(database_object)
        self.songList.append(Song(mrl, meta))
        return self.toJson()

    def database_object_to_mrl_and_meta(self, database_object):
        meta = Meta()
        meta.artist = getattr(database_object, 'artist', None)
        meta.genre = getattr(database_object, 'genre', None)
        meta.cover = getattr(database_object, 'cover', None)
        meta.title = getattr(database_object, 'title', None)
        meta.duration = getattr(database_object, 'length', None)
        mrl = getattr(database_object, 'filepath', None)
        if not mrl:
            raise Exception("Media Resource Location must be provided")
        return mrl, meta

    def add_youtube(self, url):
        yt = pafy.new(url)
        mrl, meta = self.pafy_to_mrl_and_meta(yt)
        self.songList.append(Song(mrl, meta))
        return self.toJson()

    def pafy_to_mrl_and_meta(self, pafy):
        meta = Meta()
        meta.artist = getattr(pafy, 'author', None)
        meta.genre = getattr(pafy, 'category', None)
        meta.cover = getattr(pafy, 'thumb', None)
        meta.title = getattr(pafy, 'title', None)
        meta.duration = getattr(pafy, 'length', None)
        bestAudio = pafy.getbestaudio()
        mrl = bestAudio.url
        if not mrl:
            raise Exception("Media Resource Location must be provided")
        return mrl, meta

    def get_next_mrl(self):
        if self.repeat_song:
            return self.songList[self.position].mrl
        self.position += 1
        if len(self.songList) - 1 < self.position:
            if self.repeat_queue:
                self.position = 0
            else:
                return False
        return self.songList[self.position].mrl

    def get_previous_mrl(self):
        if self.repeat_song:
            return self.songList[self.position].mrl
        elif self.position - 1 < 0:
            return self.songList[self.position].mrl
        self.position -= 1
        return self.songList[self.position].mrl

    def set_mrl_postion(self, postition):
        self.position = postition
        return self.songList[self.position].mrl

    def get_current_meta(self):
        return self.songList[self.position].meta.toJson()

    def toJson(self):
        meta = []
        for s in self.songList:
            meta.append(s.meta.__dict__)
        return json.dumps(meta)


class Song():
    def __init__(self, media_resource_location, meta):
        self.mrl = media_resource_location
        self.meta = meta


class Meta():
    def __init__(self, title=None, 
                 artist=None, 
                 genre=None, 
                 cover=None, 
                 duration=None):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.cover = cover
        self.duration = duration

    def toJson(self):
        return json.dumps(self.__dict__)

