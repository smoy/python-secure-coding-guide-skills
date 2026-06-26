# pyscg-0044: Canonicalize Input Before Validating

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-707 (pillar), CWE-180 (Validate Before Canonicalize), CWE-182 (Collapse of Data into Unsafe Value), CWE-184 (Incomplete List of Disallowed Input).

## Rule

**Normalize strings with `unicodedata.normalize()` before running any validation or pattern matching.** Unicode lookalike characters (e.g. `․` ONE DOT LEADER, `／` FULLWIDTH SOLIDUS) can bypass regex-based allow/deny lists if normalization happens after the check.

## Why

UTF-8 encodes over one million code points. Many characters are visually or semantically equivalent to ASCII punctuation but have distinct byte values. A regex looking for `./` will not match `․／` until NFKC normalization collapses them to `./`. Validating before normalizing lets attackers smuggle directory traversal sequences, XSS payloads, or other risky strings through security checks. Use `NFKC` for security-sensitive validation; be aware that `NFC`/`NFD` do not perform compatibility decomposition and will miss these equivalences.

## Non-compliant

```python
import re
import unicodedata


def api_with_ids(suspicious_string: str):
    """IDS checks BEFORE normalizing — bypass possible."""
    if re.search("./", suspicious_string):
        normalized_string = unicodedata.normalize("NFKC", suspicious_string)
        print(f"detected an attack sequence {normalized_string}")
    else:
        print("Nothing suspicious")  # reached despite malicious input


# ․ = ONE DOT LEADER, ／ = FULLWIDTH SOLIDUS
api_with_ids("․․／" * 10 + "passwd")
```

## Compliant

```python
import re
import unicodedata


def api_with_ids(suspicious_string: str):
    """Normalize FIRST, then validate."""
    normalized_string = unicodedata.normalize("NFKC", suspicious_string)
    if re.search("./", normalized_string):
        print("detected an attack sequence with . or /")
    else:
        print("Nothing suspicious")


# ․ = ONE DOT LEADER, ／ = FULLWIDTH SOLIDUS
api_with_ids("․․／" * 10 + "passwd")
```

> Cross-ref: pyscg-0045 (consistent encoding), pyscg-0047 (use allow lists over deny lists). Prefer allow lists — deny lists are a moving target.
