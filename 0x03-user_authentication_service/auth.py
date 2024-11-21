#!/usr/bin/env python3
"""Auth module."""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """A method that takes in a password
    string arguments and returns bytes."""
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password
