import logging

import vlc

from backend.player.queue import Queue

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
        self.playbackMode = "default"
        self.set_playback_mode(self.playbackMode)

        # TODO: Add playlist support
        self.queue = Queue('default')

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
        self.playing = False

    def play_pause(self):
        if self.playing is True:
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

    def set_playback_mode(self, mode):
        if mode == "loop":
            self.player.set_playback_mode(vlc.PlaybackMode.loop)
            self.playbackMode = mode
        elif mode == "repeat":
            self.player.set_playback_mode(vlc.PlaybackMode.repeat)
            self.playbackMode = mode
        elif mode == "default":
            self.player.set_playback_mode(vlc.PlaybackMode.default)
            self.playbackMode = mode
        else:
            raise NoPlaybackMode(f'{mode} is not a playbackmode')

    def get_playback_mode(self):
        return self.playbackMode


class NoPlaybackMode(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
