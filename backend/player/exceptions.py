"""This file contains all exceptions which are raised by the `player` package
"""


class NotFound(Exception):
    """Indicates that a item does not exist"""
    pass


class Duplicated(Exception):
    """Indicates that an element is already in an object"""
    pass


class EOQError(Exception):
    """Indicates the end of an queue"""
    pass
