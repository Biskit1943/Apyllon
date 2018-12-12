import logging

from flask.views import MethodView

logger = logging.getLogger(__name__)


class PlayerPlayPause(MethodView):

    def get(self):
        return "No!"

    def put(self):
        return "No!"


class PlayerNext(MethodView):

    def get(self):
        return "No!"

    def put(self):
        return "No!"


class PlayerPrevious(MethodView):

    def get(self):
        return "No!"

    def put(self):
        return "No!"


class PlayerShuffle(MethodView):

    def get(self):
        return "No!"

    def put(self):
        return "No!"


class PlayerRepeat(MethodView):

    def get(self):
        return "No!"

    def put(self):
        return "No!"
