import logging

import vlc

from queue import Queue

logging = logging.getLogger("__main__")


class Player():
    """
    Base player class, playing audio and video using libvlc
    """

    def __init__(self, queue=None):
        """
        Attributes: 
            player: holding the vlc.Mediaplayer object
        """
        self.player = vlc.MediaPlayer()
        self.playbackMode = "default"

        self.queue = Queue('default')

        self.playing = False

    def play(self):
        """
        Play the set mediafile.

        TODO:
            * Check if File is already loaded.
        """
        if str(self.player.get_state()) == "State.Paused":
            self.playing = True
            self.player.play()
        elif self.player.is_playing():
            return
        elif self.queue.get_lenght == 0:
            raise Exception("Playlist is empty")
        else:
            self.player.set_mrl(self.queue.get_next_mrl())
            self.playing = True
            self.player.play()

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
        if self.playing:
            self.player.pause()
        self.player.set_mrl(self.queue.get_next_mrl())
        self.player.play()

    def previous(self):
        pass

    def add_local(self, filepath):
        self.queue.add_local(filepath)

    def add_local_database_object(self, database_object):
        return self.queue.add_local_database_object(database_object)

    def add_youtube(self, url):
        return self.queue.add_youtube(url)

    def set_playback_mode(self, mode):
        pass

    def get_playback_mode(self):
        pass

    def get_queue_name(self):
        return self.queue.identifier

    def get_current_meta(self):
        return self.queue.get_current_meta()

    def get_playlist_meta(self):
        return self.queue.get_queue_meta()

class NoPlaybackMode(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
