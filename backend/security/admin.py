"""This file contains the wrapped routes for the admin routes in
backend/api/routes/admin.py
For the documentation on them see there
"""
from backend.security.validation import admin


@admin
def get():
    """TODO"""
    return "Returns if the admin was logged in"


@admin
def put():
    """TODO"""
    return "Changes the PW of the admin"
