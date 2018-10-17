"""This module contains all routes for communicating with the frontend"""
import os

from app import app
from app.api import (
    local,
)
from app.database.song_utils import get_songs


@app.route('/')
@app.route('/index')
def index():
    path = os.path.join(os.path.abspath('tests/test_data'))
    local.add_songs(path)
    return "Success", 200


@app.route('/list')
def ls():
    return get_songs(), 200
