#!/usr/bin/env python3
"""Auth module."""
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """A method that takes in a password
    string arguments and returns bytes."""
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates a uuid."""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """Creates a user's session id and saves it."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns the corresponding user to a session_id."""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Sets a user's session_id to None."""
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Finds the user corresponding to the email and
        generate a UUID and update the user's reset_token
        database field and Returns the token."""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Hashes the password and update the user's hashed_password field
        with the new hashed password and the reset_token field to None."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except ValueError:
            raise ValueError
