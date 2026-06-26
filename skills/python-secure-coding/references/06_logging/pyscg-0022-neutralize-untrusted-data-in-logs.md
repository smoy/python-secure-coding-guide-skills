# pyscg-0022: Neutralize Untrusted Data in Logs

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-707 (pillar), CWE-117 (Improper Output Neutralization for Logs), CWE-93 (CRLF Injection).

## Rule

Sanitize all untrusted input before writing it to application logs. Validate against a strict allow-list and neutralize CRLF sequences (`\r`, `\n`) so an attacker cannot forge additional log lines. Use `%r` formatting for rejected values to escape special characters in the log record itself.

## Why

Log injection (CAPEC-93) lets an attacker insert newline sequences into a log entry, creating fabricated records that can frame innocent users or conceal malicious activity. It can also enable XSS when logs are viewed in a vulnerable web UI. OWASP Top 10 A09:2021 lists security logging and monitoring failures as a critical risk.

## Non-compliant

```python
import logging

def log_authentication_failed(user):
    logging.warning("User login failed for: '%s'", user)

# Attacker input forges a second log line:
log_authentication_failed("guest'\nWARNING:root:User login failed for: 'administrator")
# Output includes a fake "administrator" failure log entry
```

## Compliant

```python
import logging
import re

_ALLOWED_USER = re.compile(r"^[A-Za-z0-9._-]{1,64}$")

def is_allowed_username(user: str) -> bool:
    return bool(_ALLOWED_USER.fullmatch(user))

def log_authentication_failed(user):
    if not is_allowed_username(user):
        # %r escapes CR/LF — log remains a single line
        logging.warning("Rejected login attempt: invalid username=%r", user)
        return
    logging.warning("User login failed for: '%s'", user)
```

> See also: pyscg-0019 (exclude sensitive data from logs), pyscg-0050 (sanitize error output).
