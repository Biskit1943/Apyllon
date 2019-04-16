import logging

logger = logging.getLogger(__name__)

import random as rndm
from typing import List, Union

from pytube import YouTube
from sqlalchemy.orm import Session

from backend_database.models import Songs, Playlists
from backend_database.song_utils import create as create_song
from .exceptions import Duplicated, EOQError


class AsyncQue:
    def __init__(self, identifier: int, songs: List[Songs] = None, title: str = '', pos: int = 0):
        self.id_ = identifier
        self.title = title
        self.songs = {id_: song for id_, song in enumerate(sorted(songs), 1)} if songs is not None else {}
        self.played = []
        self.song_ids = sorted([song.id_ for song in self.songs])
        self.pos = pos if pos in [s[0] for s in self.songs.items()] else 0
        self.prev = None if self.pos is 0 else self.songs.get(self.pos - 1, None)
        self.next = None if self.pos is 0 else self.songs.get(self.pos + 1, None)

    @staticmethod
    def from_playlist(playlist: Playlists):
        return AsyncQue(playlist.id_, songs=playlist.songs, title=playlist.name)

    def __len__(self):
        return len(self.songs)

    async def to_json(self):
        return {
            'id_': self.id_,
            'title': self.title,
            'songs': sorted({id_: song.to_json for id_, song in self.songs.items()}, key=lambda x: x[1].title),
            'played': self.played,
            'pos': self.pos,
            'current': self.current.to_json(),
            'next': self.next,
        }

    async def _add(self, song: Songs):
        """Adds a song to the database.

        If the ids are not in range from 1 to len(self.songs) the missing ids
        will be filled, else the id will be added to the end of the list.

        Args:
            song: The song which will be added
        """
        if not await self.check_song_in_list(song.id_):
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

    async def check_song_in_list(self, song: int):
        return song in self.song_ids

    async def add_file(
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
        song = await create_song(
            filepath=filepath,
            artist=artist,
            title=title,
            album=album,
            genre=genre,
            length=length,
            db=db
        )

        try:
            await self._add(song)
        except Duplicated:
            raise

        if ret:
            return await self.to_json()

    async def add_db(self, song: Songs, ret: bool = False):
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
            await self._add(song)
        except Duplicated:
            raise

        if ret:
            return await self.to_json()

    async def add_youtube(self, url: str, ret: bool = False, db: Session = None):
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
        yt_song = yt.streams.filter(only_audio=True).first()
        best_url = yt_song.url
        title = yt.title
        song = await create_song(filepath=best_url, title=title, length=int(yt.length), db=db)

        try:
            await self._add(song)
        except Duplicated:
            raise

        if ret:
            return self.to_json()

    def get_next(self, *, loop: bool = False, random: bool = False):
        """Returns the next item in the queue.

        If the end of the queue is reached and loop is False, an exception is
        raised.
        If random is True, a random element is picked

        Args:
            loop (bool, optional): If True, the queue will start from the beginning
            random (bool, optional): If True, a random song is picked

        Returns:
            The next song which will be played
        """
        if self.next is None and self.pos is not 0:
            raise EOQError('No next item available')
        elif self.pos is not 0:
            logger.info(f'self.pos is not 0, current = {self.next}')
            current = self.next  # next song is already defined
        else:
            try:
                self.pos = 1
                current = self.songs[self.pos]
                logger.info(f'self.pos is 0, current = {self.songs[self.pos]}')
            except IndexError:  # only if songs is empty
                raise

        if not random:  # no random element choice
            self.pos += 1
            if self.pos > len(self.songs):
                logger.info(f'{self.pos} is greater than {len(self.songs)}')
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
            yield self.get_next(loop=loop, random=random)
            if not self.next:
                break

    def get_prev(self):
        current = self.prev
        self.next = self.current
        self.pos = self.played.pop()
        return current

    @property
    def current(self) -> Songs:
        return self.songs[self.pos]
