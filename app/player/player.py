import vlc
import pafy
import time
import spotipy

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

class YoutubePlayer(Player):
    """
    Modified Player to play youtube videos as Audio.
    """

    def __init__(self):
        """
        Call parent constructor.
        """
        Player.__init__(self)

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
