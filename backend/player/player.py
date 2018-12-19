import vlc
import pafy
import time
from backend.player.queue import Queue
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
    def __init__(self, queue=None):
        """
        Attributes: 
            player: holding the vlc.Mediaplayer object
        """
        self.player = vlc.MediaListPlayer()

        #TODO: Add playlist suppoert
        self.queue=Queue('default')

        self.player.set_media_list(self.queue.media_list)

        self.playing = False
    
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

    def previous(self):
        self.player.previous()

    def add_local(self, filepath):
        self.queue.add_local(filepath)

    def add_youtube(self, url):
        self.queue.add_youtube(url)

    def set_playback_mode(self, mode):
        if mode == "loop":
            self.player.set_playback_mode(vlc.PlaybackMode.loop)
        elif mode == "repeat":
            self.player.set_playback_mode(vlc.PlaybackMode.repeat)
        elif mode == "default":
            self.player.set_playback_mode(vlc.PlaybackMode.default)
        else:
            raise NoPlaybackMode(f'{mode} is not a playbackmode')


class NoPlaybackMode(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
