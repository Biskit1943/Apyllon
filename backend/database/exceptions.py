"""This file contains all exceptions which are raised by the `database`
package
"""


class Exists(Exception):
    """Indicates that a resource already exist"""
    pass


class MultipleReturned(Exception):
    """Indicates that a recourse exist more than one which shouldn't be"""
    pass


class DoesNotExist(Exception):
    """Indicates that a resource already exist"""
    pass

