#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class definition."""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the
        Authorization header for Basic Auth."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes a base64 authorization header and
        returns the decoded value as a UTF-8 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_value
        except (TypeError, base64.binascii.Error):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header:
            str) -> (str, str):
        """Extracts user credentials from a
        decoded Base64 string (email:password)"""
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password
