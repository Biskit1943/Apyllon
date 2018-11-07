"""This file contains the Database models for sql"""
from typing import Dict

from backend import db

song_playlist_association = db.Table('song_playlist',
                                     db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
                                     db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
                                     )


class Admin(db.Model):
    """Describes the admin

    Attributes:
        id: The id of this object (managed by the database)
        username: The username which was chosen, defaults to `admin`
        password_hash:  The password hash from the admin
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, default='admin')
    password_hash = db.Column(db.String(88))


class User(db.Model):
    """Describes a user

    Attributes:
        uid: The id of this object (managed by the database)
        username: The username which was chosen by the user
        password_hash:  The password hash from the user
    """
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(88))
    playlists = db.relationship("Playlist", back_populates="owner", uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self) -> Dict:
        """Transforms the database information into a dict

        Returns:
            A dict with all the song data, see the function for the schema
        """
        user = {
            'uid': self.uid,
            'username': self.username,
        }
        return user


class Song(db.Model):
    """Describes a song

    Attributes:
        id: The id of this object (managed by the database)
        filepath_id: The id of the Filepath table
        filepath: The Filepath table which holds the filepath
        artist: The artist of the song
        title: The title of the song
        genre: The genre(s) of the song in lowercase (eg. rap/hip-hop)
        length: The seconds of the song
    """
    sid = db.Column(db.Integer, primary_key=True)
    filepath_id = db.Column(db.Integer, db.ForeignKey('filepath.id'))
    filepath = db.relationship("Filepath", back_populates="song")
    artist = db.Column(db.String(64))
    title = db.Column(db.String(64))
    album = db.Column(db.String(64))
    genre = db.Column(db.String(32))
    length = db.Column(db.Integer)

    def __repr__(self):
        return f'<Song {self.filepath.filename}>'

    def to_dict(self) -> Dict:
        """Transforms the database information into a dict

        Returns:
            A dict with all the song data, see the function for the schema
        """
        song = {
            'sid': self.sid,
            'filename': self.filepath.filename,
            'path': self.filepath.directory,
            'length': self.length,
            'meta': {
                'artist': self.artist,
                'title': self.title,
                'album': self.album,
                'genre': self.genre,
            },
        }
        return song


class Filepath(db.Model):
    """Describes the path to a song on the local filesystem

    Attributes:
        id: The id of this object (managed by the database)
        filename: The name of the file
        directory: The path to the directory of the file
        song: The song which has this filepath
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), nullable=False)
    directory = db.Column(db.Text, nullable=False)
    song = db.relationship("Song", uselist=False, back_populates="filepath")

    def __repr__(self):
        return f'<SongFile {self.directory}/{self.filename}>'


class Playlist(db.Model):
    """Describes a Playlist of an User

    Attributes:
        id: The id of this object (managed by the database)
        owner: The user which owns this playlist
        songs: The songs of which this playlist consists
    """
    id = db.Column(db.Integer, primary_key=True)
    owner = db.relationship("User", back_populates="playlists")
    songs = db.relationship("Song",
                            secondary=song_playlist_association,
                            backref="playlists")

    def __repr__(self):
        return f'<Playlist {id} with {len(self.songs.all())} songs>'
