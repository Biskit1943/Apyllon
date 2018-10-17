"""This file contains the Database models for sql"""
from app import db


class Admin(db.Model):
    """Describes the admin

    Attributes:
        id: The id of the admin (managed by the database)
        username: The username which was chosen, defaults to `admin`
        password_hash:  The password hash from the admin
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, default='admin')
    password_hash = db.Column(db.String(128))


class User(db.Model):
    """Describes a user

    Attributes:
        id: The id of the user (managed by the database)
        username: The username which was chosen by the user
        password_hash:  The password hash from the user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'


class Song(db.Model):
    """Describes a song

    Attributes:
        id: The id of the song (managed by the database)
        filename: The name of the file
        directory: The directory where the file is saved
        artist: The artist of the song
        title: The title of the song
        genre: The genre(s) of the song in lowercase (eg. rap/hip-hop)
        length: The seconds of the song
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), nullable=False)
    directory = db.Column(db.Text, nullable=False)
    artist = db.Column(db.String(64))
    title = db.Column(db.String(64))
    genre = db.Column(db.String(32))
    length = db.Column(db.Integer)

    def __repr__(self):
        return f'<Song {self.filename}>'
