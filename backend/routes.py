"""This module contains all routes for communicating with the frontend"""
import logging
import os

from backend import (
    app,
    db,
)
from backend.api import (
    local,
)
from backend.api.routes import (
    users,
    player,
)
from backend.database.song_utils import list_songs

logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/index')
def index():
    path = os.path.join(os.path.abspath('tests/test_data'))
    local.add_songs(path)
    return "Success", 200


@app.route('/list')
def ls():
    return list_songs()


@app.teardown_appcontext
def shutdown_session(exception=None):
    logger.debug('disconnect from db session')
    db.session.remove()


# User related endpoints
app.add_url_rule('/users',
                 view_func=users.UserView.as_view(name='user'),
                 methods=['GET', 'POST', ]
                 )
app.add_url_rule('/users/<int:uid>',
                 view_func=users.UsersIdView.as_view(name='users_id'),
                 methods=['GET', 'PUT', 'DELETE', ]
                 )
app.add_url_rule('/users/<string:username>',
                 view_func=users.UsersNameView.as_view(name='users_name'),
                 methods=['GET', 'PUT', 'DELETE', ]
                 )
app.add_url_rule('/users/<int:uid>/authenticate',
                 view_func=users.UsersIdAuthView.as_view(name='users_id_auth'),
                 methods=['POST', ]
                 )
app.add_url_rule('/users/<string:username>/authenticate',
                 view_func=users.UsersNameAuthView.as_view(name='users_name_auth'),
                 methods=['POST', ]
                 )
app.add_url_rule('/users/changepw',
                 view_func=users.UsersNameChangePassword.as_view(name='users_change_password'),
                 methods=['PUT'])

# Player related endpoints
app.add_url_rule('/player/play-pause',
                 view_func=player.PlayerPlayPause.as_view(name='player_play_pause'),
                 methods=['PUT', 'GET', ]
                 )
app.add_url_rule('/player/next',
                 view_func=player.PlayerNext.as_view(name='player_next'),
                 methods=['PUT', 'GET', ]
                 )
app.add_url_rule('/player/previous',
                 view_func=player.PlayerPrevious.as_view(name='player_previous'),
                 methods=['PUT', 'GET', ]
                 )
app.add_url_rule('/player/shuffle',
                 view_func=player.PlayerShuffle.as_view(name='player_shuffle'),
                 methods=['PUT', 'GET']
                 )
app.add_url_rule('/player/loop',
                 view_func=player.PlayerLoop.as_view(name='player_repeat'),
                 methods=['PUT', 'GET']
                 )
