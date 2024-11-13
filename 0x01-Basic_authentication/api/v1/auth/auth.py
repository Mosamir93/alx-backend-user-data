#!/usr/bin/env python3
"""Auth class module."""
from typing import List, TypeVar
from flask import request


class Auth:
    """Class definition."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if requires auth."""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Returns None."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None."""
        return None
