#!/usr/bin/env python3
"""Session expiration auth module."""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Class definition."""
    def __init__(self):
        """Constructor."""
        try:
            duration = int(getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """Creates a session id."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id,
                              "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload gets the user_id for session_id."""
        session_dict = self.user_id_by_session_id.get(session_id, None)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at', None)
        if created_at is None:
            return None
        if created_at + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None
        return session_dict.get('user_id')
