import pafy

class media():
    def __init__(self, path, meta=None):
        path = path
        meta = meta

class local_media(media):
    def __init__(self, path, meta=None):
        super().__init__(path, meta)

class youtube_media(media):
    def __init__(self, url, meta=None):
        video = pafy.new(url)
        bestaudio = video.getbestaudio(bestaudio.url)
        super().__init__(path=bestaudio, meta=meta)

        
