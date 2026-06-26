# pyscg-0015: Handle Error Conditions

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-703 (pillar), CWE-755 (Improper Handling of Exceptional Conditions).

## Rule

Always wrap I/O and OS operations in `try/except` blocks. Catch the relevant exception, then respond, log, or recover explicitly — never let operations fail silently or swallow errors with `missing_ok=True` without a handler.

## Why

Unhandled `OSError` / `FileNotFoundError` crashes the program without a meaningful message. Silent suppression (e.g., `unlink(missing_ok=True)` with no logging) hides operational failures and makes debugging impossible.

## Non-compliant

```py
import os, uuid

def read_file(file):
    fd = os.open(file, os.O_RDONLY)   # raises OSError if file missing
    content = os.read(fd)              # no cleanup on error
    return content.decode()

read_file(f"{uuid.uuid4()}.txt")       # crashes silently
```

## Compliant

```py
import os, uuid

def read_file(file):
    try:
        fd = os.open(file, os.O_RDONLY)
        try:
            content = os.read(fd, 1024)
        finally:
            os.close(fd)
        return content.decode()
    except OSError as e:
        if not os.path.exists(file):
            print(f"File not found: {file}")
        elif os.path.isdir(file):
            print(f"Is a directory: {file}")
        else:
            print(f"An error occurred: {e}")

read_file(f"{uuid.uuid4()}.txt")
```

> See also: pyscg-0016 (propagate exceptions), pyscg-0052 (cleanup on exceptions).
