#!/usr/bin/env python3
"""Auth module."""
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """A method that takes in a password
    string arguments and returns bytes."""
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a db instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user to the database after hashing the password."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if mail and password match a valid user."""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False
