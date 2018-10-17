import vlc
import pafy
import time

class Player():

    def __init__(self):
        self.player = vlc.MediaPlayer()

    def load(self, filepath):
        self.player.set_mrl(filepath)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

class YoutubePlayer(Player):

    def __init__(self):
        Player.__init__(self)

    def load(self, url):
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        self.player.set_mrl(bestaudio.url)

class SpotifyPlayer(Player):
    pass
