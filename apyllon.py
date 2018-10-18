"""This Modules provides a WSGI for the Flask backend"""
from gevent import pywsgi

from backend import app


def main():
    """Creates and runs the WSGI-Server"""
    print("Starting server...")
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
