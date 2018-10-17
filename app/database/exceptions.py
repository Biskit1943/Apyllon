"""This file contains all exceptions which are raised by the `database`
package
"""


class Exists(Exception):
    """Indicates that a resource already exist"""
    pass
