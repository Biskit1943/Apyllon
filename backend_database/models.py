from json import dumps
from typing import List

from pytube import YouTube
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from config import get_type
from . import Base

__all__ = [
    'Users',
    'Playlists',
    'Songs',
]


class Users(Base):
    __tablename__ = 'Users'
    id_ = Column('id', Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String(72), nullable=False)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return f'<{"Admin" if self.admin else "User"} {self.username}>'

    def __str__(self):
        return dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id_,
            'username': self.username,
            'admin': self.admin,
        }


class Songs(Base):
    __tablename__ = 'Songs'
    id_ = Column('id', Integer, primary_key=True)
    type_ = Column(Integer, index=True)
    filepath = Column(String, unique=True)
    artist = Column(String(32))
    title = Column(String(64))
    album = Column(String(32))
    genre = Column(String(32))
    length = Column(Integer)

    def __repr__(self):
        return f'<Song {self.artist} - {self.title}>'

    def __str__(self):
        return dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id_,
            'type': get_type(self.type_, str),
            'filepath': self.filepath,
            'meta': {
                'artist': self.artist,
                'title': self.title,
                'album': self.album,
                'genre': self.genre,
            },
            'length': self.length,
        }

    def get_stream(self):
        if self.type_ is 1:
            return self.filepath
        elif self.type_ is 2:
            yt = YouTube(self.filepath)
            yt_song = yt.streams.filter(only_audio=True).first()
            best_url = yt_song.url
            return best_url


song_playlist_association_table = Table(
    'song_playlist_association', Base.metadata,
    Column('song_id', Integer, ForeignKey('Songs.id')),
    Column('playlist_id', Integer, ForeignKey('Playlists.id'))
)


class Playlists(Base):
    __tablename__ = 'Playlists'
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(32))
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship("Users", backref="playlists")
    songs = relationship('Songs', secondary=lambda: song_playlist_association_table, backref="playlists")

    def __repr__(self):
        return f'<Playlist {self.name}>'

    def __str__(self):
        return dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id_,
            'title': self.name,
            'user_id': self.user_id,
            'user': self.user.to_dict(),
            'songs': [s.to_dict() for s in self.songs],
        }

    def add(self, *, song: Songs, songs: List[Songs]):
        if song and song not in self.songs:
            self.songs.append(song)
        elif songs:
            for song in songs:
                if song not in self.songs:
                    self.songs.append(song)
