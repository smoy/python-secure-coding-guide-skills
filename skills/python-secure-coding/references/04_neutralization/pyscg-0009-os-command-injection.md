# pyscg-0009: Prevent OS Command Injection

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-707 (pillar), CWE-78 (Improper Neutralization of Special Elements Used in an OS Command).

*Overlaps the security-guidance plugin (the reactive/detective layer); this is the proactive Python-idiom complement.*

## Rule

Avoid passing untrusted input into OS commands via `subprocess`, `os.system`, or similar. Prefer Python-native modules (`pathlib`, `shutil`, `os`) that perform the equivalent operation without invoking a shell. When a subprocess is unavoidable, use `shell=False` with a list argument and never build the command string by concatenation.

## Why

`shell=True` passes the command to `/bin/sh -c` (or `cmd.exe /C`), meaning any shell metacharacter (`;`, `&`, `|`, backtick) in untrusted input executes an additional command. Even `shell=False` with `find -exec` can be abused when a folder name itself is attacker-controlled. The safest mitigation is to replace the shell command entirely with a Python equivalent that never invokes a subprocess.

## Non-compliant

```python
from subprocess import Popen
import os

class FileOperations:
    def list_dir(self, dirname: str):
        if "nt" in os.name:
            Popen("dir " + dirname, shell=True).communicate()   # injectable
        if "posix" in os.name:
            Popen("ls " + dirname, shell=True).communicate()    # injectable

# Attacker injects: "/etc/shadow; head -1 /etc/passwd"
FileOperations().list_dir("/etc/shadow; head -1 /etc/passwd")
```

## Compliant

```python
import os
from pathlib import Path

def list_dir(dirname: str):
    path = Path(dirname)
    allowed_directory = Path.home()
    # Resolves symlinks; raises ValueError if dirname escapes allowed_directory
    if Path(
        allowed_directory.joinpath(dirname)
        .resolve()
        .relative_to(allowed_directory.resolve())
    ):
        for item in path.glob("*"):
            print(item)
```

`pathlib.Path.glob()` never invokes a shell; attacker-controlled characters in `dirname` are treated as data, not commands. The `relative_to()` check prevents directory traversal.

## See also

- pyscg-0047 (allow lists over deny lists for input validation)
- pyscg-0012 (archive extraction — a common vector for injected file names)
