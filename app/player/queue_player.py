import vlc
import pafy
import time
from abc import ABC
"""
TODO: 
    * Exceptions []
    * Playlists? []
    * Test []
"""

class Player():
    """
    Base player class, playing audio and video using libvlc
    """
    def __init__(self):
        """
        Attributes: 
            player: holding the vlc.Mediaplayer object
        """
        self.player = vlc.MediaPlayer()
        self.queue = []
        self.playing = False

    def load(self, filepath):
        """
        Load a file to and set as vlc mediafile.
        
        Args:
            filepath (string): Path to the file to play.
        """
        self.player.set_mrl(filepath)

    def play(self):
        """
        Play the set mediafile.

        TODO:
            * Check if File is already loaded.
        """
        self.player.play()

    def stop(self):
        """
        Stop the set mediafile.

        """
        self.player.stop()

    def pause(self):
        """
        Pause the set mediafile.

        """
        self.player.pause()

    def load(self, url):
        """
        Overides the default load method of Player object.
        Uses pafy to get the url for the best availible audiostream.
        Args:
            url (string): the url for the youtube video to play
        """
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        self.player.set_mrl(bestaudio.url)

    def media_fatory(media_resource_locator, source, meta=None):

        class media(ABC):

            @abstractmethod
            def __init__(self, media_resource_locator, meta):
                pass

            @abstractmethod
            def get_media_resource_locator(self):
                pass

            @abstractmethod
            def get_meta(self):
                pass

        class youtube_audio(media):

            def __init__(self, media_resource_locator, meta):
                self.me

        if source is "local":
            pass
        elif source is "youtube":
            pass
        else:
            pass
