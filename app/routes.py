"""This module contains all routes for communicating with the frontend"""
from app import app
from app.api import (
    local,
)


@app.route('/')
@app.route('/index')
def index():
    local.add_songs('test')
