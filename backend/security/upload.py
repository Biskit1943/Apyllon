import logging
import os

from flask import request, jsonify
from werkzeug.utils import secure_filename

from config import Config

logger = logging.getLogger(__name__)


def u_post():
    if 'file' not in request.files:
        logger.error('Upload with no files in body')
        return jsonify('No files were given'), 400

    uploaded_files = [request.files["file"]]
    logger.debug(f'Received files: {uploaded_files}')

    for file in uploaded_files:
        try:
            if file.filename == '':
                logger.error('File with no name uploaded')
                return jsonify('Filename empty'), 400

            if _allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(Config.HOME, filename))
                logger.debug(f'saved file {file} to disk')
            else:
                return jsonify(f'wrong file format {file.filename}'), 415
        except Exception as e:
            logger.critical(f'Error while uploading new files: {e}')
            return jsonify(f'Error while uploading files: {e}'), 500

    return jsonify('Success'), 200


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.SONG_EXTENSIONS
