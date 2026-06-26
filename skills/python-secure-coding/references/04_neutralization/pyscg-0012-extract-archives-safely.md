# pyscg-0012: Extract Archives Safely

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-409 (Improper Handling of Highly Compressed Data / Data Amplification), CWE-180 (Incorrect Behavior Order: Validate Before Canonicalize), CWE-209 (Generation of Error Message Containing Sensitive Information).

## Rule

Before extracting any archive from an untrusted source: (1) validate that every member path stays within a designated base directory (zip slip), (2) check actual extracted size — not just metadata — against a maximum (zip bomb), and (3) limit the total number of entries.

## Why

Zip slip attacks embed relative paths like `../../../bin/bash` to overwrite files outside the intended extraction directory. Zip bomb attacks exploit high compression ratios or forged metadata to cause disk exhaustion or memory overflow. `zipfile.extractall()` performs no path or size checks; `ZipInfo.file_size` is attacker-controlled metadata and cannot be trusted alone — the actual size must be verified by reading the decompressed bytes.

## Non-compliant

```python
import zipfile

# extractall() applies no path or size constraints
with zipfile.ZipFile("archive.zip", mode="r") as zf:
    zf.extractall()                     # zip slip and zip bomb both succeed
```

Also non-compliant: trusting `member.file_size` from `infolist()` — that field comes from zip metadata and can be forged to bypass size checks while the actual decompressed content is larger.

## Compliant

```python
import zipfile
from pathlib import Path

MAXSIZE = 100 * 1024 * 1024   # 100 MB per file
MAXAMT  = 1000                 # max entries in archive

class ZipExtractException(Exception):
    pass

def path_validation(filepath: Path, base_path: Path):
    resolved = (base_path / filepath).resolve()
    if not str(resolved).startswith(str(base_path.resolve())):
        raise ZipExtractException(f"Path traversal detected: {resolved}")

def extract_files(filepath: str, base_path: str):
    with zipfile.ZipFile(filepath, mode="r") as archive:
        if len(archive.infolist()) > MAXAMT:
            raise ZipExtractException(f"Too many entries (limit {MAXAMT})")
        for item in archive.infolist():
            if item.file_size > MAXSIZE:           # early metadata check
                raise ZipExtractException(f"Metadata reports oversized: {item.filename}")
            path_validation(Path(item.filename), Path(base_path))
        Path(base_path).mkdir(exist_ok=True)
        for item in archive.infolist():
            if item.is_dir():
                Path(base_path).joinpath(item.filename).resolve().mkdir(exist_ok=True)
                continue
            with archive.open(item.filename) as fh:
                data = fh.read(MAXSIZE + 1)
                if len(data) > MAXSIZE:            # reality check on actual bytes
                    raise ZipExtractException(f"Actual size exceeds limit: {item.filename}")
                out = Path(base_path).joinpath(fh.name).resolve()
                out.write_bytes(data)
```

## See also

- pyscg-0044 (canonicalize input before validating — required for thorough path normalization)
- pyscg-0009 (OS command injection — crafted file names can also inject shell commands)
