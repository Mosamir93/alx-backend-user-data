#!/usr/bin/env python3
"""Auth class module."""
from typing import List, TypeVar
from flask import request
from os import getenv


class Auth:
    """Class definition."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if requires auth."""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns None."""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None."""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request."""
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
