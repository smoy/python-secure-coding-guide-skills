# pyscg-0013: Secure Search Paths

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-426 (Untrusted Search Path).

## Rule

Launch Python with the `-I` (isolated) flag to suppress attacker-controlled `PYTHONPATH` and `PYTHONHOME` overrides, and add `--check-hash-based-pycs always` to enforce byte-code integrity. Never rely on the default timestamp-based `.pyc` validation in environments where an attacker might control the filesystem or environment variables.

## Why

Python resolves modules by searching `sys.path`, which includes `PYTHONPATH` from the environment. An attacker who can set `PYTHONPATH` can inject a shadow module (e.g., a fake `http/server.py`) that is loaded instead of the standard library module. Additionally, Python's default `.pyc` validation only checks timestamp + file size, so a manipulated `PYTHONPYCACHEPREFIX` can cause a tampered byte-code file to be loaded silently. Hash-based verification (PEP 552) computes a SHA-256 digest of the source file and compares it to the digest stored in the `.pyc` header, catching substitution even when the timestamp matches.

## Non-compliant

```bash
# PYTHONPATH is not suppressed; byte code is validated by timestamp only
python3 -m http.server -b 127.0.0.42 8080
```

An attacker who can write to the filesystem and set `PYTHONPATH=$HOME/evil/` can replace `http.server` with arbitrary code.

## Compliant

```bash
# -I isolates from PYTHONPATH/PYTHONHOME; --check-hash-based-pycs always
# verifies .pyc integrity against source hash
python3 -I --check-hash-based-pycs always -m http.server -b 127.0.0.42 8080
```

## Exception

This control is not required when untrusted entities have no ability to modify environment variables or any Python source/byte-code files on the host (ENV-4P-EX0).
