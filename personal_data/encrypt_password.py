#!/usr/bin/env python3
"""Hash and validate passwords using bcrypt."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return a salted, hashed version of password as a byte string."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Return True if password matches hashed_password, else False."""
    return bcrypt.checkpw(password.encode(), hashed_password)
