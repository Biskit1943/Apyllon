from flask import jsonify

from backend import app


class BadRequest(Exception):
    status_code = 400

    def __init__(self, message, payload=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        rv = {'expected': dict(self.payload or ()), 'error': self.message}
        return rv


class Conflict(Exception):
    status_code = 409

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        rv = {'error': self.message}
        return rv


# ============================================================================ #
#                                 errorhandler                                 #
# ============================================================================ #
@app.errorhandler(BadRequest)
@app.errorhandler(Conflict)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
