import logging
import vlc
from backend.player.queue import Queue
import threading
import time


logging = logging.getLogger("__main__")


class Player:
    """
    Base player class, playing audio and video using libvlc
    """

    def __init__(self, queue=None):
        """
        Attributes: 
            player: holding the vlc.Mediaplayer object
        """
        self.player = vlc.MediaPlayer()
        self.queue = Queue('default')
        self.playing = False
        observer = threading.Thread(target=self.observer)
        observer.start()

    def observer(self):
        while True:
            position = self.player.get_position()
            if position >= 0.01:
                self.player.stop()
                time.sleep(1)
                self.next()
            time.sleep(1)

    def play(self):
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
        next_mrl = self.queue.get_next_mrl()
        if not next_mrl:
            self.playing = False
            self.player.stop()
        else:
            self.player.set_mrl(next_mrl)
            self.player.play()

    def previous(self):
        if self.playing:
            self.player.pause()
        self.player.set_mrl(self.queue.get_previous_mrl())
        self.player.play()

    def add_local(self, filepath):
        self.queue.add_local(filepath)

    def add_local_database_object(self, database_object):
        return self.queue.add_local_database_object(database_object)

    def add_youtube(self, url):
        return self.queue.add_youtube(url)

    def set_playback_mode(self, mode):
        modes = [self.queue.repeat_queue,
                 self.queue.repeat_song,
                 self.queue.shuffle]
        map(lambda x: False, modes)
        if mode == "repeat_song":
            self.queue.repeat_song = True
        elif mode == "repeat_queue":
            self.queue.repeat_queue = True
        elif mode == "shuffle":
            self.queue.shuffle = True

    def get_playback_mode(self):
        modes = [self.queue.repeat_queue,
                 self.queue.repeat_song,
                 self.queue.shuffle]
        mode = filter(lambda x: x is True, modes)
        return mode

    def get_queue_name(self):
        return self.queue.identifier

    def get_current_meta(self):
        return self.queue.get_current_meta()

    def get_playlist_meta(self):
        return self.queue.get_queue_meta()

    def get_current_track_lenght(self):
        return self.player.get_length()

    def get_current_track_position(self):
        return self.player.get_time()

    def get_current_track_postion_percentage(self):
        return self.player.get_position()

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def get_volume(self):
        return self.player.audio_get_volume()

    def set_queue_track(self, track_number):
        if self.playing:
            self.player.pause()
        next_mrl = self.queue.set_mrl_postion(track_number)
        if not next_mrl:
            self.playing = False
            self.player.stop()
        else:
            self.player.set_mrl(next_mrl)
            self.player.play()
