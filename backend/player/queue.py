import logging

logger = logging.getLogger(__name__)

import random as rndm
from typing import List, Union

from pytube import YouTube
from sqlalchemy.orm import Session

from config import SongTypes
from backend_database.models import Songs, Playlists, Users
from backend_database.song_utils import create as create_song
from backend_database.playlist_utils import create as create_playlist
from backend_database.playlist_utils import get as get_playlist
from backend_database.playlist_utils import append as append_to_playlist
from .exceptions import Duplicated, EOQError


class Queue:
    def __init__(self, identifier: int, songs: List[Songs] = None, title: str = 'Default', pos: int = 0):
        self.id_ = identifier
        self.title = title
        self.songs = {id_: song for id_, song in enumerate(sorted(songs), 1)} if songs is not None else {}
        self.played = []
        self.song_ids = sorted([song.id_ for song in self.songs])
        self.pos = pos if pos in [s[0] for s in self.songs.items()] else 0
        self.prev = None if self.pos is 0 else self.songs.get(self.pos - 1, None)
        self.next = None if self.pos is 0 else self.songs.get(self.pos + 1, None)
        self.loop = False
        self.shuffle = False

    @staticmethod
    def from_playlist(playlist: Playlists):
        return Queue(playlist.id_, songs=playlist.songs, title=playlist.name)

    def __len__(self):
        return len(self.songs)

    def is_empty(self):
        return len(self) == 0

    def to_dict(self):
        songs = {id_: song.to_dict() for id_, song in self.songs.items()}
        return {
            'id_': self.id_,
            'title': self.title,
            'songs': songs,
            # 'songs': sorted({id_: song.to_dict for id_, song in self.songs.items()}, key=lambda x: x[1].title),
            'played': self.played,
            'pos': self.pos,
            'current': None if not self.current else self.current.to_dict(),
            'next': self.next,
        }

    def _add(self, song: Songs):
        """Adds a song to the database.

        If the ids are not in range from 1 to len(self.songs) the missing ids
        will be filled, else the id will be added to the end of the list.

        Args:
            song: The song which will be added
        """
        if not self.check_song_in_list(song.id_):
            if self.songs == {}:
                self.songs[1] = song
                self.song_ids.append(song.id_)
                return
            sorted_songs = sorted(self.songs.items(), key=lambda x: x[0])
            last_song = sorted_songs[-1]  # (id_: song)
            song_id = len(self.songs) + 1

            if len(self.songs) < last_song[0]:  # check if the ids are complete
                for i, id_ in enumerate([s[0] for s in sorted_songs], 1):
                    # iterate over all ids till we find the missing
                    if i != id_:
                        song_id = i
                        break

            self.songs[song_id] = song
            if song_id in self.played:
                self.played.remove(song_id)
            self.song_ids.append(song.id_)
        else:
            raise Duplicated(f'{song} is already in this Queue')

    def check_song_in_list(self, song: int):
        return song in self.song_ids

    def add_file(
            self,
            *,
            filepath: str,
            artist: str = None,
            title: str = None,
            album: str = None,
            genre: str = None,
            length: int,
            db: Session = None,
            ret: bool = False,
    ) -> Union[None, dict]:
        """Adds a File to the Queue, which may or may not already exist in the
        database.

        Args:
            filepath (str): The path to the file on the LOCAL filesystem
            artist (str, optional): The artist(s) of the song
            title (str, optional): The title of the song (if not provided the
                filepath is taken)
            album (str, optional): The album in which this song appeared
            genre (str, optional): The genre of the song
            length (int): The length of the song
            db (Session, optional): If provided, save song to database on
                creation
            ret (bool, optional): If set to True, return `func`:self.to_json:

        Raises:
            Duplicated: If the song is already in this queue

        Returns:
            If ret is True `func`:self.to_json: which returns a dict
            representing this object
        """
        song = create_song(
            type_=SongTypes.FILE.value,
            filepath=filepath,
            artist=artist,
            title=title,
            album=album,
            genre=genre,
            length=length,
            db=db
        )

        try:
            self._add(song)
        except Duplicated:
            raise

        if ret:
            return self.to_dict()

    def add_db(self, song: Songs, ret: bool = False):
        """Adds a song from the database to this queue.

        Args:
            song (Songs): The song object which will be added to the queue
            ret (bool, optional): If set to True, return `func`:self.to_json:

        Raises:
            Duplicated: If the song is already in this queue

        Returns:
            If ret is True `func`:self.to_json: which returns a dict
            representing this object
        """
        try:
            self._add(song)
        except Duplicated:
            raise

        if ret:
            return self.to_dict()

    def add_youtube(self, url: str, ret: bool = False, db: Session = None):
        """Adds a YouTube song to the Queue, which may or may not already exist
        in the database.

        Args:
            url (str): The url of the YouTube video
            db (Session, optional): If provided, save song to database on
                creation
            ret (bool, optional): If set to True, return `func`:self.to_json:

        Returns:
            If ret is True `func`:self.to_json: which returns a dict
            representing this object
        """
        yt = YouTube(url)
        title = yt.title
        if not title:
            logger.info('Failed to get title from Video URL')
        song = create_song(type_=SongTypes.YOUTUBE.value, filepath=url, title=title, length=int(yt.length), db=db)

        try:
            self._add(song)
        except Duplicated:
            raise

        if ret:
            return self.to_dict()

    def get_next(self, *, loop: bool = None, shuffle: bool = None) -> Songs:
        """Returns the next item in the queue.

        If the end of the queue is reached and loop is False, an exception is
        raised.
        If loop is True, a random element is picked

        Once loop or shuffle set, it will be saved till it is overridden.

        Args:
            loop (bool, optional): If True, the queue will start from the beginning
            shuffle (bool, optional): If True, a random song is picked

        Returns:
            The next song which will be played
        """
        if shuffle is None:
            shuffle = self.shuffle
        else:
            self.shuffle = shuffle

        if loop is None:
            loop = self.loop
        else:
            self.loop = loop

        if self.next is None and self.pos is not 0:
            raise EOQError('No next item available')
        elif self.pos is not 0:
            logger.debug(f'self.pos is not 0, current = {self.next}')
            logger.info('getting next song from Playlist')
            current = self.next  # next song is already defined
        else:
            try:
                self.pos = 1  # first index is 1
                current = self.songs[self.pos]
                logger.debug(f'self.pos was 0, starting from beginning')
                logger.info(f'starting Playlist from beginning, current = {self.songs[self.pos]}')
            except IndexError:  # only if songs is empty
                raise

        if shuffle is False:  # no random element choice
            self.pos += 1
            if self.pos > len(self.songs):
                logger.debug(f'next position would be {self.pos}, but Playlist only has {len(self.songs)} songs')
                logger.info('Playlist exceeded')
                self.played = []
                self.pos = 0
                if not loop:
                    self.next = None  # No next item available
                    return current  # Return last available item
                else:
                    self.pos = 1

            logger.info(f'setting next to {self.pos}')
            self.next = self.songs.get(self.pos, None)
        else:
            choices = [song[0] for song in self.songs if song[0] not in self.played]
            if len(choices) == 0:
                self.played = []
                self.pos = 0
                if not loop:
                    self.next = None  # No next item available
                    return current  # Return last available item
                else:
                    choices = [song[0] for song in self.songs]

            choice = rndm.choice(choices)
            self.played.append(choice)
            self.pos = choice
            self.next = self.songs.get(choice, None)
        logger.info(f'returning current {current}')
        return current

    def all(self, *, loop: bool = False, random: bool = False):
        while True:
            yield self.get_next(loop=loop, shuffle=random)
            if not self.next:
                break

    def get_prev(self):
        self.pos = self.pos - 1 if self.pos > 0 else self.pos
        current = self.songs.get(self.pos)
        self.next = self.songs.get(self.pos + 1) if len(self.songs) > self.pos else None
        return current

    @property
    def current(self) -> Songs:
        return self.songs.get(self.pos)

    def to_playlist(self, current_user: Users, name: str = None, db: Session = None):
        self.title = name if name is not None else self.title
        if db:
            if name is None and self.title == '':
                raise RuntimeError('This should never happen')
            if self.id_ is -1:
                playlist = create_playlist(
                    user=current_user, name=name, songs=[song for _, song in self.songs.items()], db=db)
                self.id_ = playlist.id_
            else:
                playlist = get_playlist(self.id_, db=db)
                if not playlist:
                    self.id_ = -1
                    logger.error('Cannot find this Playlist id!')
                elif playlist.songs in [song for _, song in self.songs.items()]:
                    logger.info('Updating Playlist')
                    missing = [song for _, song in self.songs.items()] - playlist.songs
                    print(missing)
                    # append_to_playlist(playlist, songs=missing, db=db)
                else:
                    logger.info('Playlist up to date')

        data = self.to_dict()
        songs = data.get('songs')
        indexed_songs = []
        for index, song in songs.items():
            indexed_songs.append(
                {
                    'index': index,
                    'length': song.get('length', -1),
                    'meta': song.get('meta'),
                }
            )
        print(indexed_songs)
        return {'title': data.get('title'), 'songs': indexed_songs}
