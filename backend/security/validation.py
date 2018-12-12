"""This file contains all security related wrapper functions for the routes."""
import logging
from typing import Callable

from decorator import decorator

logger = logging.getLogger(__name__)


@decorator
def _user_validation(func: Callable, *args, **kwargs):
    """This wrapper will validate the JWT. On failure it will automatically
    return the corresponding message and error-code for the API.

    This wrapper is for API usage only and should only be used here!
    """
    # TODO validate
    return func(*args, **kwargs)
