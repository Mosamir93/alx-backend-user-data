#!/usr/bin/env python3
"""Filtered logger."""
from typing import List, Tuple
import mysql.connector
import os
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Class constructor."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum."""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Function that takes no arguments and returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root",
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or "",
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost",
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    connector = mysql.connector.connect(user=user,
                                        password=password,
                                        host=host,
                                        database=database)
    return connector


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
