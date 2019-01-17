"""This module provides utilities for the filepath table in the database"""
import logging
import os

from backend import db
from backend.database.exceptions import DoesNotExist
from backend.database.models import (
    Filepath,
)

logger = logging.getLogger(__name__)


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


def get_filepath(path: str) -> Filepath:
    """Returns the filepath object which corresponds to the given path

    Args:
        path: The path to a file
    Returns:
        The filepath object which has the given path
    Raises:
        DoesNotExist when the path was not found in the database
    """
    directory, filename = os.path.split(path)
    filepath = Filepath.query.filter(db.and_(
        Filepath.filename == filename,
        Filepath.directory == directory)).first()
    if not filepath:
        logger.error(f'Filepath not found in database: {path}')
        raise DoesNotExist(f'No such file in database: {path}')
    return filepath
