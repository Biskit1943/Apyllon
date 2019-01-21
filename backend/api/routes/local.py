import logging

from flask.views import MethodView

from backend.security.upload import u_post
from backend.security.update import update

logger = logging.getLogger(__name__)


class UploadView(MethodView):

    def post(self):
        u_post()


class UpdateView(MethodView):

    def put(self):
        update()
