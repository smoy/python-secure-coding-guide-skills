---
name: python-secure-coding
description: >-
  Secure-coding guidance for Python (CPython >= 3.9), adapted from the OpenSSF
  Secure Coding Guide for Python. Use when writing, reviewing, or refactoring
  Python that touches numeric precision/overflow, money or measurement math,
  bit manipulation, loop counters, security-sensitive randomness (tokens,
  secrets, keys, nonces, session IDs, passwords — NOT random test data,
  sampling, or simulations), cryptographic values, encoding/locale, input
  neutralization (command/SQL/format-string injection, deserialization, unsafe
  archive extraction, path/search-path safety, allow-lists), exception
  handling, secure logging (sensitive-data exposure, log injection, error
  disclosure), access control, or thread/process concurrency
  (ThreadPoolExecutor, locks, thread pools). Apply these rules proactively while
  generating Python code, and cite the pyscg rule + CWE when flagging an issue.
  Complements the security-guidance plugin (which reactively reviews diffs) by
  shaping code as it is written.
---

# Python Secure Coding (OpenSSF-derived)

Proactive, Python-specific secure-coding rules. This is the **generative** layer:
apply it while writing Python so insecure idioms never get written. The
`security-guidance` plugin remains the **detective** layer that reviews diffs —
for the thin overlap (marked † below: command/SQL/format-string injection,
deserialization) defer to the plugin and cross-reference rather than re-flag.

Each rule is `pyscg-XXXX`. When you act on one, name the rule and its CWE. Full
detail + compliant/non-compliant examples live in `references/<domain>/`.
**Load a reference file only when its rule is actually relevant** (progressive
disclosure) — don't read them all up front. Reference files often list the full
CWE chain; the cheat-sheet below shows the primary CWE only.

## Domains (all 9 shipped, 42 rules)

`01_introduction` · `02_encoding_and_strings` · `03_numbers` ·
`04_neutralization`† · `05_exception_handling` · `06_logging` ·
`07_concurrency` · `08_coding_standards` · `09_cryptography`

## Fast heuristics

- `import random` near a token/password/key/session/nonce → pyscg-0038 (use `secrets`).
- `float` in money math or an `==` on computed values → pyscg-0001 / pyscg-0004.
- `<<` / `>>` doing multiply/divide → pyscg-0003 (mind precedence: `8 << 2 + 10` ≠ `(8<<2)+10`).
- `numpy`/`ctypes`/`math.exp`/`datetime` on attacker-sized values → pyscg-0002.
- `ThreadPoolExecutor` → pyscg-0024 (interruptible), 0025 (bounded), 0026 (no nested interdependent submits).
- `subprocess`/`os.system`, `shell=True`, SQL string-building, `str.format()` on user data, `pickle.loads` → 04_neutralization†.
- bare `except:` / swallowed errors / `assert` used as a real check → 05_exception_handling, pyscg-0037.
- logging anything user-derived or secret → 06_logging (0019 secrets, 0022 log injection, 0050 error disclosure).
- hard-coded credentials, client-trusted roles → pyscg-0041, pyscg-0055.

## Rule index (by domain)

Trigger = when to pull the reference. Paths are under `references/`.

### 01_introduction
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0040 | Run each trust zone under a separate OS user/process | mixing trust levels in one process | CWE-501 |
| 0041 | Never hard-code credentials; inject config/secrets at deploy | secrets or config literals in source | CWE-798 |
| 0042 | Use explicit conditionals; one write per statement | complex bitwise/boolean expressions | CWE-783 |
| 0055 | Derive identity & roles server-side only | handlers trusting client-supplied roles | CWE-472 |

### 02_encoding_and_strings
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0043 | Set locale explicitly before locale-dependent ops | `strftime`/`atof`/locale-sensitive ops | CWE-175 |
| 0044 | Canonicalize (NFKC) before validating | regex/allow-list validation of untrusted strings | CWE-180 |
| 0045 | Use UTF-8 end-to-end; don't silently transcode | data crossing encoding boundaries | CWE-176 |

### 03_numbers
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0001 | Use `int` (cents) or `Decimal`, not `float`, for exact values | money, tax, equality-compared computed values | CWE-1339 |
| 0002 | Catch overflow on fixed-width numbers | `numpy`/`ctypes`/`datetime`/`math.exp` | CWE-190 |
| 0003 | Prefer `*`/`/` over `<<`/`>>` for arithmetic | bit-shifts used as multiply/divide | CWE-1335 |
| 0004 | Use `int` loop counters; convert to `float` at use | fractional-step `while`/accumulator loops | CWE-197 |

### 04_neutralization †
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0008 † | Use `string.Template`; user input ≠ format template | `str.format()` built from user data | CWE-134 |
| 0009 † | Replace shell with `pathlib`/`shutil`; never `shell=True` | `subprocess`/`os.system` + untrusted input | CWE-78 |
| 0010 † | Parameterized queries; no `executescript()` on user data | SQL assembled from user input | CWE-89 |
| 0011 | Explicitly cast external values; type hints aren't runtime guards | C interop / untyped external input | CWE-843 |
| 0012 | Validate path + real size + entry count before extracting | extracting an untrusted archive | CWE-409 |
| 0013 | Launch `python -I`; control `PYTHONPATH` | attacker-controllable `PYTHONPATH` | CWE-426 |
| 0023 † | Prefer JSON; if pickle, HMAC-sign before `loads()` | deserializing across a trust boundary | CWE-502 |
| 0047 | Reject everything not on an explicit allow list | validating HTML/SQL/paths/args | CWE-184 |

### 05_exception_handling
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0014 | Raise specific exception types, never bare `Exception` | raising exceptions | CWE-397 |
| 0015 | Wrap I/O in `try/except`; never fail silently | file/OS ops without handling | CWE-755 |
| 0016 | No bare `except`; re-raise with `from` to preserve context | swallowed/bare excepts | CWE-396 |
| 0018 | Use `math.isnan`/`isfinite` after `float()` | accepting float input from outside | CWE-754 |
| 0028 | No `return`/`break`/`continue` inside `finally` | `try/finally` blocks | CWE-584 |
| 0052 | Use `with` for guaranteed cleanup | lock/file/socket/connection acquisition | CWE-460 |

### 06_logging
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0019 | Never log passwords, secrets, or personal data | log statements touching credentials/PII | CWE-532 |
| 0020 | Use the `logging` module; forward to a central system | exceptions / security-relevant events | CWE-778 |
| 0021 | Strip debug modes & diagnostic ports before shipping | deploying/packaging an app | CWE-489 |
| 0022 | Allow-list and escape CRLF in user data before logging | logging any user-derived value | CWE-117 |
| 0050 | Generic error + correlation ID; detail logged server-side | errors returned to clients | CWE-209 |

### 07_concurrency
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0024 | Make pool tasks check a `threading.Event` | `ThreadPoolExecutor` + cancellation/shutdown | CWE-400 |
| 0025 | Bound concurrency with `max_workers` + timeout/cancel; no thread-per-request | request/message handlers spawning threads | CWE-410 |
| 0026 | Don't submit interdependent/nested tasks to one bounded pool | `submit()` then `.result()` on same executor | CWE-833 |

### 08_coding_standards
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0031 | Iterate over a copy; modify the original outside the loop | mutating list/dict/set inside a `for` | CWE-1095 |
| 0032 | Don't reuse built-in/stdlib names as identifiers | naming things `len`, `os`, `str`, … | CWE-1109 |
| 0033 | Implement `__eq__`; compare with `==`, not `is` | custom-class equality / membership tests | CWE-595 |
| 0034 | Guard against `None` before use | optional args / external input | CWE-476 |
| 0035 | `NamedTemporaryFile` with `with`; leave no temp files | creating temporary files | CWE-459 |
| 0036 | Capture return values; check sentinels (e.g. `-1`) | immutable-method / sentinel-returning calls | CWE-252 |
| 0037 | Raise exceptions for real checks, not `assert` (stripped by `-O`) | validation / security guards | CWE-617 |
| 0051 | Explicitly release OS-backed resources when done | file handles, sockets, DB connections | CWE-404 |

### 09_cryptography
| Rule | Do this | Trigger | CWE |
|------|---------|---------|-----|
| 0038 | Use `secrets` (not `random`) for security-sensitive values | tokens/keys/passwords/nonces | CWE-330 |

---

† Overlaps the `security-guidance` plugin. The plugin reactively reviews diffs;
these rules add the proactive Python-idiom fix. Cross-reference, don't duplicate.

See `ATTRIBUTION.md` for licensing (CC-BY-4.0 docs / MIT code, OpenSSF). The
maintainer-only `scripts/sync-from-upstream.sh` (at the repo root, outside this
skill) refreshes the upstream cache for re-adaptation; the skill never runs it.
