import vlc
import pafy
import time
from abc import ABC

import logging 
import os
logging = logging.getLogger("__main__")

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
        self.playing = False
        logging.info("Initialise Player()")

    def load(self, filepath):
        """
        Load a file to and set as vlc mediafile.
        
        Args:
            filepath (string): Path to the file to play.
        """
        self.player.set_mrl(filepath)
        logging.info("Loading Mediafile: " + str(filepath))

    def play(self):
        """
        Play the set mediafile.

        TODO:
            * Check if File is already loaded.
        """
        self.player.play()
        self.playing = True
        logging.info("Starting media play")

    def stop(self):
        """
        Stop the set mediafile.

        """
        self.player.stop()
        self.playing = False
        logging.info("Stoping media play")

    def pause(self):
        """
        Pause the set mediafile.

        """
        self.player.pause()
        self.plaing = False
        logging.info("Pausing media play")

    def load_youtube(self, url):
        """
        Overides the default load method of Player object.
        Uses pafy to get the url for the best availible audiostream.
        Args:
            url (string): the url for the youtube video to play
        """
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        self.player.set_mrl(bestaudio.url)
        logging.info("Loading Mediafile from youtube url:  " + str(url))

