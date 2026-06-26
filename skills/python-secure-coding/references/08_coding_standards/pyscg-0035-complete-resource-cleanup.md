# pyscg-0035: Complete Resource Cleanup

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-459 (Incomplete Cleanup).

## Rule

Always delete temporary files after use. Use `tempfile.NamedTemporaryFile()` as a context manager (the default `delete=True` removes the file on exit) rather than creating plain files or using `tempfile.mkstemp()` without explicit cleanup.

## Why

Temporary files that are never deleted accumulate on disk, leading to resource exhaustion and potential denial of service. A `finally` block alone is insufficient because abnormal process termination may skip it. `tempfile.NamedTemporaryFile()` with the `with` statement guarantees deletion even on exceptions, and creates the file with restrictive permissions (owner read/write only).

## Non-compliant

```python
# Plain file: never deleted
f = open("tempfile.txt", "w")
f.write("temporary file created!")
f.close()

# mkstemp: secure creation, but no automatic cleanup
import os
from tempfile import mkstemp

fd, path = mkstemp()
with os.fdopen(fd, 'w') as f:
    f.write('TEST\n')
# path still exists on disk after this block
```

## Compliant

```python
import tempfile

# File is automatically deleted when the 'with' block exits
with tempfile.NamedTemporaryFile() as temp_file:
    temp_file.write(b'This temporary file will be deleted.')
    temp_file_path = temp_file.name

# Attempting to open temp_file_path here raises FileNotFoundError — correct behaviour
```

> To keep the file accessible after the `with` block (e.g. pass it to a subprocess), set `delete_on_close=False` (Python 3.12+) and delete it explicitly when done.
