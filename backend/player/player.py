"""
"A media resource locator (MRL) is a string of characters used to identify a
multimedia resource or part of a multimedia resource. A MRL may be used to
identify inputs or outputs to VLC media player."
https://wiki.videolan.org/Media_resource_locator/
"""
import asyncio
import logging

logger = logging.getLogger(__name__)

from enum import Enum

import vlc
from sqlalchemy.orm import Session

from backend_database.models import Playlists
from .queue import AsyncQue


class PlayerState(Enum):
    PLAY = 'play'
    STOP = 'stop'
    PAUSE = 'pause'


class AsyncPlayer:
    def __init__(self, playlist: Playlists = None):
        self.queue = AsyncQue.from_playlist(playlist) if playlist else AsyncQue(1)  # TODO get next id from db
        self.vlc = vlc.MediaPlayer()
        self.state = PlayerState.PAUSE

    def observer(self):
        while True:
            if not self.vlc.is_playing() and self.state is PlayerState.PLAY:
                logger.info('next song')
                self.play()
            asyncio.sleep(1)

    async def _play(self, song: str):
        self.vlc.set_mrl(song)
        self.state = PlayerState.PLAY
        logger.info('play')
        if not self.vlc.play():
            logger.error('error while playing the song')
        while True:
            if not self.vlc.is_playing:
                return
            await asyncio.sleep(1)

    async def play(self, song: str = None):
        logger.info('play orig')
        if self.state is PlayerState.PLAY:
            return
        elif not song and not self.queue:
            return
        elif song:
            await self._play(song)
        else:
            for song in self.queue.all():
                await self._play(song.filepath)

    async def pause(self):
        if self.state is not PlayerState.PLAY:
            return
        else:
            self.vlc.pause()

    def stop(self):
        if self.state is not PlayerState.PLAY:
            return
        else:
            self.vlc.stop()

    async def add_youtube(self, url: str, ret: bool = False, db: Session = None):
        song = await self.queue.add_youtube(url, ret, db)
        if ret:
            return song


class Player:
    """
    Base player class, playing audio and video using libvlc
    """

    def __init__(self, queue: int = None):
        self.player = vlc.MediaPlayer()
        self.playing = False

    def play(self):
        if str(self.player.get_state()) == "State.Paused":
            self.playing = True
            self.player.play()
        elif self.player.is_playing():
            return
        elif self.queue.get_length == 0:
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
        pass

    def get_queue_name(self):
        return self.queue.identifier

    def get_current_meta(self):
        return self.queue.get_current_meta()

    def get_playlist_meta(self):
        return self.queue.get_queue_meta()

    def get_current_track_length(self):
        pass

    def get_current_track_position(self):
        pass

    def get_current_track_position_percentage(self):
        pass

    def set_volume(self, volume):
        pass

    def get_volume(self, volume):
        pass

    def set_queue_track(self, track_number):
        pass


class NoPlaybackMode(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)
