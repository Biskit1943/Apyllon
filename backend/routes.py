"""This module contains all routes for communicating with the frontend"""
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
)
from backend.database.song_utils import list_songs


@app.route('/')
@app.route('/index')
def index():
    path = os.path.join(os.path.abspath('tests/test_data'))
    local.add_songs(path)
    return "Success", 200


@app.route('/list')
def ls():
    return list_songs(), 200


@app.teardown_appcontext
def shutdown_session(exception=None):
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
