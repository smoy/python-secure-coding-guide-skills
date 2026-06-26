# pyscg-0020: Implement Informative Event Logging

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-693 (pillar), CWE-778 (Insufficient Logging).

## Rule

Log security-relevant events (authentication attempts, authorization failures, data access) using Python's `logging` module with appropriate severity levels. Never rely on `print()` to `stdout`/`stderr` for security events. Forward logs to a remote, centralized logging service so they survive host compromise.

## Why

Printing errors to `stdout`/`stderr` is unreliable (buffers can be exhausted or closed) and the output may be visible to untrusted parties. Log files stored only locally can be deleted by an attacker. Without proper logging, incident response and forensic reconstruction become impossible. Swallowed or raw exceptions may also inadvertently leak sensitive internal details.

## Non-compliant

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("Error occurred:", e)  # raw exception to stdout — not centralized, leaks detail
```

## Compliant

```python
import logging

try:
    result = 10 / 0
except ZeroDivisionError:
    logging.critical("Error occurred: Division by zero")
    # Production: configure log forwarding to a remote logging service
```

> See also: pyscg-0019 (exclude sensitive data from logs), pyscg-0050 (sanitize error output).
