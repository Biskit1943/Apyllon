import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    REQUIRED_META_DATA = [
        'artist',
        'title',
        'album',
        'genre',
    ]
    SONG_EXTENSIONS = [
        '.mp3',
        '.mp4',
        '.wav',
    ]

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
