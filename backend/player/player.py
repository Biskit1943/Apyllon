import vlc
import pafy
import time
from queue import Queue
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

        if(not queue):
            self.queue=Queue('default')
        else:
            self.queue=queue

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

    def stop(self):
        """
        Stop the set mediafile.

        """
        self.player.stop()
        self.playing = False

    def pause(self):
        """
        Pause the set mediafile.

        """
        self.player.pause()
        self.plaing = False

    def play_pause(self):
        if self.plaing is True:
            self.pause()
        else:
            self.play()

    def next(self):
        self.player.next()

    def previous(self):
        self.player.previous()

    def add_local(self, filepath):
        self.queue.add_local(filepath)

    def add_youtube(self, url):
        self.queue.add_youtube(url)
