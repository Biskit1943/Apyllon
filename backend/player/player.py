"""
"A media resource locator (MRL) is a string of characters used to identify a
multimedia resource or part of a multimedia resource. A MRL may be used to
identify inputs or outputs to VLC media player."
https://wiki.videolan.org/Media_resource_locator/
"""
import logging
import threading
import time

logger = logging.getLogger(__name__)

from enum import Enum

import vlc
from sqlalchemy.orm import Session

from backend_database.models import Playlists, Songs
from .queue import Queue


class PlayerState(Enum):
    PLAY = 'play'
    STOP = 'stop'
    PAUSE = 'pause'


class Player:
    def __init__(self, playlist: Playlists = None):
        self.queue = Queue.from_playlist(playlist) if playlist else None
        self.song = None

        # VLC setup
        self.vlc_instance = vlc.Instance()
        # this is the actual playing object
        self.vlc_media_player = self.vlc_instance.media_player_new()
        self.events = self.vlc_media_player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next)

        self.state = PlayerState.STOP
        # this object take care about play/pause/stop events
        self.player = threading.Thread(target=self.observer, daemon=True)
        self.player.start()

    def observer(self):
        while True:
            if self.state is PlayerState.PLAY and not self.vlc_media_player.is_playing():
                logger.debug('<=== play ===>')
                if self.vlc_media_player.play() is -1:
                    logger.error('error while playing')
            elif self.state is PlayerState.PAUSE and self.vlc_media_player.is_playing():
                logger.info('<=== pause ===>')
                self.vlc_media_player.pause()
            elif self.state is PlayerState.STOP and self.vlc_media_player.is_playing():
                logger.info('<=== stop ===>')
                self.vlc_media_player.stop()
            time.sleep(0.5)

    def play(self, song: str = None):
        if self.state is PlayerState.PLAY:
            return self.get_state()

        if not song and not self.queue:
            logger.error('nothing to play')
            return
        elif song:
            self.vlc_media_player.set_mrl(song)
            self.queue = None
        elif not self.vlc_media_player.get_media():
            self.next()

        self.state = PlayerState.PLAY
        return self.get_state()

    def pause(self):
        if self.state is PlayerState.PLAY:
            self.state = PlayerState.PAUSE
            return self.get_state()

    def stop(self):
        if self.state is PlayerState.PLAY:
            self.state = PlayerState.STOP
            return self.get_state()

    def next(self, *args, **kwargs):
        if not self.queue:
            logger.error('No queue, nothing next to play...')
            return
        self.vlc_media_player.set_mrl(self.queue.get_next().get_stream())

    def get_position(self):
        return self.vlc_media_player.get_position()

    def get_state(self):
        if self.queue and not self.queue.is_empty():
            return {
                'loop': self.queue.loop,
                'state': self.state,
                'next': self.queue.next,
                'previous': self.queue.prev,
                'shuffle': self.queue.shuffle,
                'queue_or_song': self.queue.current,
            }
        else:
            return {
                'queue_or_song': self.song,
            }

    def set_queue(self, queue: Queue):
        # reset player for new queue
        self.vlc_media_player = self.vlc_instance.media_player_new()
        self.events = self.vlc_media_player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next)
        self.state = PlayerState.STOP

        self.queue = queue

    def add_youtube(self, url: str, ret: bool = False, db: Session = None):
        if not self.queue:
            self.queue = Queue(-1)  # create temp queue
        song = self.queue.add_youtube(url, ret, db)
        if ret:
            return song

    def add_song(self, song: Songs):
        if not self.queue:
            self.queue = Queue(-1)  # create temp queue
        self.queue.add_db(song)
