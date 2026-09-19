# Personal Data

Advanced Python Programming | ALU BSE

## Description

This project covers handling Personally Identifiable Information
(PII) responsibly: redacting sensitive fields out of log messages,
connecting to a database using credentials from environment variables
(never hard-coded), and securely hashing and validating passwords.

## Files

| File | Description |
|------|-------------|
| `filtered_logger.py` | `filter_datum` — regex-based redaction of specified fields in a log line. `RedactingFormatter` — a `logging.Formatter` subclass that redacts PII fields in every log record it formats. `get_logger` — returns a configured `"user_data"` logger (INFO level, no propagation, `RedactingFormatter` with `PII_FIELDS`). `get_db` — connects to the `users` MySQL table using credentials from environment variables. `main` — reads all rows from `users` and logs each one, redacted. |
| `encrypt_password.py` | `hash_password` — salts and hashes a password with `bcrypt`. `is_valid` — checks a plaintext password against a bcrypt hash. |

## Learning Objectives

- What Personally Identifiable Information (PII) is, and why certain
  fields (names, emails, phone numbers, SSNs, passwords, etc.) must
  never appear in plaintext in logs.
- How to write a log filter that redacts specific fields using a
  single regex substitution (`filter_datum`), and how to plug that
  into a custom `logging.Formatter` so every log line is redacted
  automatically, without changing how the rest of the application
  logs.
- Why database credentials should never be hard-coded or committed to
  version control, and how to read them from environment variables
  instead (with sane defaults where appropriate).
- Why passwords must never be stored in plaintext, even in a
  database: `bcrypt.hashpw` produces a salted hash, and
  `bcrypt.checkpw` verifies a plaintext password against that hash
  without ever needing to store or compare the plaintext itself.

## Requirements

- Ubuntu 18.04 LTS, Python 3.7 (`python3`)
- Every file starts with `#!/usr/bin/env python3`, ends with a newline,
  and is executable
- pycodestyle compliant
- Every module, class, and function has a real documentation string
- `bcrypt` and `mysql-connector-python` must be installed
  (`pip3 install bcrypt mysql-connector-python`)

## Environment variables (for `get_db` / `main`)

| Variable | Default |
|----------|---------|
| `PERSONAL_DATA_DB_USERNAME` | `root` |
| `PERSONAL_DATA_DB_PASSWORD` | `""` (empty) |
| `PERSONAL_DATA_DB_HOST` | `localhost` |
| `PERSONAL_DATA_DB_NAME` | *(no default — required)* |
