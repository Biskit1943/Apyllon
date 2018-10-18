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

    SWAGGER = {
        'title': 'Apyllon - A multi-user music player',
        'doc_dir': os.path.join(os.getcwd(), 'backend', 'templates', 'swagger')
    }

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
