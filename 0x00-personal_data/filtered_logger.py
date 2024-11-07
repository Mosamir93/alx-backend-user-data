#!/usr/bin/env python3
"""Filtered logger."""
from typing import List
import re
import logging


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """A function that  returns the log message obfuscated"""
    for field in fields:
        message = re.sub("{}=[^{}]+".format(field, separator),
                         "{}={}".format(field, redaction),
                         message)
    return message
