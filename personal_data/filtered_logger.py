#!/usr/bin/env python3
"""Filter and redact PII from log messages, and log from a database."""
import logging
import os
import re
from typing import List, Tuple

import mysql.connector


PII_FIELDS: Tuple[str, str, str, str, str] = (
    "name", "email", "phone", "ssn", "password",
)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscate the values of the given fields in a log message.

    Args:
        fields: field names whose values should be obfuscated.
        redaction: string to replace each field's value with.
        message: the log line to obfuscate.
        separator: character separating fields in the message.

    Returns:
        The log message with each field's value replaced by redaction.
    """
    pattern = r"(" + "|".join(fields) + r")=[^" + separator + r"]*"
    return re.sub(pattern, r"\1=" + redaction, message)


class RedactingFormatter(logging.Formatter):
    """Logging Formatter that redacts PII fields in log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with the list of fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record, redacting the configured PII fields."""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Return a logging.Logger configured to redact PII fields.

    The logger is named "user_data", logs up to INFO level, does not
    propagate to other loggers, and uses a StreamHandler with a
    RedactingFormatter parameterized with PII_FIELDS.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a connector to the secure users database.

    Credentials are read from the environment variables
    PERSONAL_DATA_DB_USERNAME (default "root"),
    PERSONAL_DATA_DB_PASSWORD (default ""),
    PERSONAL_DATA_DB_HOST (default "localhost"), and
    PERSONAL_DATA_DB_NAME (no default).
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name,
    )


def main() -> None:
    """Retrieve all rows from the users table and log them, redacted."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [column[0] for column in cursor.description]

    logger = get_logger()

    for row in cursor:
        message = "; ".join(
            "{}={}".format(field, value)
            for field, value in zip(field_names, row)
        ) + ";"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
