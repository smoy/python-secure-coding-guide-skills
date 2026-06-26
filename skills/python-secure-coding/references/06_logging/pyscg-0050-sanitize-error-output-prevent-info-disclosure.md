# pyscg-0050: Sanitize Error Output to Prevent Information Disclosure

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-209 (Error Message Containing Sensitive Information), CWE-532 (Sensitive Info in Log File), CWE-497 (Exposure of System Data).

## Rule

Split error information: send detailed diagnostic data (full traceback, file paths, exception type) only to the trusted back-end log; return a generic error with a unique correlation ID to the client. Validate and canonicalize file paths to block path traversal before any file operation.

## Why

Raw exceptions expose internal structure to attackers: `FileNotFoundError` reveals filesystem layout, `sqlite3.DataError` reveals schema, `PermissionError` reveals existing paths. Even a generic `BaseException` without detail still tells an attacker that a probed path exists — enabling brute-force enumeration. CVE-2022-27177 (ConsoleMe format string) shows how error leakage can escalate to RCE.

## Non-compliant

```python
from pathlib import Path

class FileReader:
    def __init__(self, args: list[str]):
        path = Path(Path.home(), args[0])
        fh = open(path, 'r', encoding="utf-8")  # raw PermissionError leaks full path
        fh.readlines()

FileReader(["Documents"])
# Output: PermissionError: [Errno 13] Permission denied: 'C:\Users\user1\Documents'
```

## Compliant

```python
from pathlib import Path
import os
import random
import logging

def file_reader(args: list):
    filepath = Path(os.path.realpath(Path(Path.home(), args[0])))
    try:
        if Path.home() not in filepath.parents:
            raise PermissionError("Invalid file")  # block path traversal
        _ = filepath.read_text(encoding='utf8')
    except (PermissionError, IsADirectoryError):
        error_id = f"{random.getrandbits(64):16x}"
        logging.exception("ERROR %s", error_id)          # full detail to back-end log only
        print(f"ERROR {error_id}: Unable to retrieve file '{filepath.stem}'")  # generic to client

file_reader(["Documents"])
```

> See also: pyscg-0019 (exclude sensitive data from logs), pyscg-0022 (neutralize untrusted data in logs), pyscg-0020 (informative event logging).
