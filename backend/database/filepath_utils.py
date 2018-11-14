"""This module provides utilities for the filepath table in the database"""
import logging

logger = logging.getLogger('__main__')

from backend import db
from backend.database.models import (
    Filepath,
)


def is_unique(filename: str, directory: str) -> bool:
    """Checks whether a filename/directory combination is unique

    Args:
        filename: The filename
        directory: The path to the file
    """
    logger.debug(f'is_unique({filename}, {directory})')
    if len(Filepath.query.filter(db.and_(
            Filepath.filename == filename,
            Filepath.directory == directory)).all()) > 0:
        logger.debug(f'{directory}/{filename} is not unique')
        return False
    logger.debug(f'{directory}/{filename} is unique')
    return True
