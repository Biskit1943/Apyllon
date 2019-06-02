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
from backend_database.song_utils import get_youtube_url

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
        # self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next)

        self.state = PlayerState.STOP.value
        # this object take care about play/pause/stop events
        self.player = threading.Thread(target=self.observer, daemon=True)
        self.player.start()

    def observer(self):
        while True:
            if self.state == PlayerState.PLAY.value and not self.vlc_media_player.is_playing():
                logger.debug('<=== play ===>')
                if self.vlc_media_player.play() is -1:
                    logger.error('error while playing')
            elif self.state == PlayerState.PAUSE.value and self.vlc_media_player.is_playing():
                logger.info('<=== pause ===>')
                self.vlc_media_player.pause()
            elif self.state == PlayerState.STOP.value and self.vlc_media_player.is_playing():
                logger.info('<=== stop ===>')
                self.vlc_media_player.stop()
            time.sleep(0.5)

    def play(self, song: Songs = None):
        if self.state == PlayerState.PLAY.value and not song:
            return self.get_state()
        elif self.state == PlayerState.PLAY.value and song:
            self.stop()

        if not song and not self.queue:
            logger.error('nothing to play')
            return self.get_state()
        elif song:

            self.vlc_media_player.set_mrl(get_youtube_url(song.filepath))
            self.vlc_media_player.play()
            self.queue = None
        elif not self.vlc_media_player.get_media():
            self.next()

        self.state = PlayerState.PLAY.value
        return self.get_state()

    def pause(self):
        if self.state == PlayerState.PLAY.value:
            self.state = PlayerState.PAUSE.value
            return self.get_state()

    def stop(self):
        if self.state == PlayerState.PLAY.value:
            self.state = PlayerState.STOP.value
            return self.get_state()

    def next(self, *args, **kwargs):
        if not self.queue:
            logger.error('No queue, nothing next to play...')
            return self.get_state()
        self.vlc_media_player.set_mrl(self.queue.get_next().get_stream())
        return self.get_state()

    def prev(self, *args, **kwargs):
        if not self.queue:
            logger.error('No queue, nothing previous to play...')
            return self.get_state()
        self.vlc_media_player.set_mrl(self.queue.get_prev().get_stream())
        return self.get_state()

    def shuffle(self, *args, **kwargs):
        if not self.queue:
            logger.error('No queue, nothing to shuffle...')
            return self.get_state()
        self.queue.shuffle = not self.queue.shuffle
        return self.get_state()

    def loop(self, *args, **kwargs):
        if not self.queue:
            logger.error('No queue, nothing to loop...')
            return self.get_state()
        self.queue.loop = not self.queue.loop
        return self.get_state()

    def get_position(self):
        return self.vlc_media_player.get_position()

    def get_state(self):
        if self.queue and not self.queue.is_empty():
            return {
                'loop': self.queue.loop,
                'state': self.state,
                'next': self.queue.next.to_dict() if self.queue.next is not None else None,
                'current': self.queue.current.to_dict() if self.queue.current is not None else None,
                'previous': self.queue.prev.to_dict() if self.queue.prev is not None else None,
                'shuffle': self.queue.shuffle,
                'queue_or_song': self.queue.current.to_dict() if self.queue.current is not None else None,
            }
        else:
            return {
                'state': self.state,
                'queue_or_song': self.song,
            }

    def set_queue(self, queue: Queue):
        # reset player for new queue
        self.vlc_media_player = self.vlc_instance.media_player_new()
        self.events = self.vlc_media_player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next)
        self.state = PlayerState.STOP.value

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
