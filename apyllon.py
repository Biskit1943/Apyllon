"""This Modules provides a WSGI for the Flask backend"""
import logging.config

from logger import logging_config

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

from gevent import monkey

monkey.patch_all()

from gevent import pywsgi

from backend import app
from backend.database.admin_utils import create_admin


def main():
    """Creates and runs the WSGI-Server"""
    logger.info("Check if admin exists")
    admin, token = create_admin()
    logger.info(f"TOKEN: {token}")

    logger.info("Starting server...")
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, log=logger)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
