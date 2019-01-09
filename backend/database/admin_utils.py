"""Utility for the user table in the database.
All user related actions which involve the database belong here, except the
ones which deal with security. The security related functions can be found in
`backend/security/user.py`.
"""
import logging
import secrets
import string
from hashlib import blake2b
from typing import (
    Dict,
    Tuple,
)

from backend import db
from backend.database.exceptions import Exists
from backend.database.models import User
from backend.security import jwt

logger = logging.getLogger(__name__)


def create_admin() -> Tuple[User, Dict]:
    """Creates the admin if he does not exist yet or set the random password
    if he exist. If the user already changed the password this function will
    throw an error.

    Returns:
        A tuple containing the new created Admin object and a dict containing
        the admin information with the generated JWT
    """
    logger.debug(f'Creating admin')

    admin = User.query.filter_by(uid=1).first()
    if admin and admin.username != "admin":
        logger.critical("Raising error")
        raise RuntimeError("The user with the id 1 exists but the name is not admin")

    if admin and admin.password:
        logger.debug(f'Admin already exist and password already changed')
        token = jwt.gen_jwt(password=admin.password_hash, username="admin")
        return admin, token

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(20))
    logger.info(f'''
################################################################################
#                    Copy this Password and login as admin.                    #
#                  After that immediately change the password!                 #
#                                                                              #
#                             {password}                             #
#                                                                              #
################################################################################''')
    password_hash = blake2b(password.encode()).hexdigest()

    if admin:
        admin.password_hash = password_hash
    else:
        admin = User(uid=1, username="admin", password_hash=password_hash)
        db.session.add(admin)

    db.session.commit()
    logger.info("Created admin")

    token = jwt.gen_jwt(password=password_hash, username="admin")

    return admin, token
