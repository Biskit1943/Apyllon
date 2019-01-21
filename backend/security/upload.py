import logging
import os

from flask import request
from werkzeug.utils import secure_filename

from config import Config

logger = logging.getLogger(__name__)


def u_post():
    if 'file' not in request.files:
        logger.error('Upload with no files in body')
        return 'No files were given', 400

    uploaded_files = request.files.getlist("file[]")
    logger.debug(f'Received files: {uploaded_files}')

    for file in uploaded_files:
        if file.filename == '':
            logger.error('File with no name uploaded')
            return 'Filename empty', 400

        if _allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.HOME, filename))
            logger.debug(f'saved file {file} to disk')
    else:
        return 'Success', 200


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.SONG_EXTENSIONS
