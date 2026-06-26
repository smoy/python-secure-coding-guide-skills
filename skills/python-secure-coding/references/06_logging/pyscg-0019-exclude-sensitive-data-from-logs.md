# pyscg-0019: Exclude Sensitive Data From Logs

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-359 (Privacy Violation), CWE-532 (Insertion of Sensitive Information into Log File).

## Rule

Never log passwords, security answers, or other secret credentials. Encrypt or anonymize personal data (usernames, dates of birth, etc.) before logging. Set log levels to `WARNING` or higher in production — never ship code with `DEBUG` enabled, as debug logs often capture sensitive fields.

## Why

Log files are frequently stored, forwarded to central systems, and accessed by multiple operators. Leaking secrets or personal data in logs violates privacy regulations (GDPR, CCPA) and creates a persistent, hard-to-remediate exposure. Cross-border log forwarding adds additional compliance risk.

## Non-compliant

```py
import logging

def login_user(username, password, security_question):
    logging.info(
        "User %s login attempt: password=%s, security answer=%s",
        username, password, security_question
    )
```

## Compliant

```py
import logging

def login_user(username, password, security_question):
    # Log only the non-sensitive username; never log password or security answer
    logging.info("User %s login attempt", username)
```

> See also: pyscg-0022 (neutralize untrusted data in logs), pyscg-0050 (sanitize error output).
