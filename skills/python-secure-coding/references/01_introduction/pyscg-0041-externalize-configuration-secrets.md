# pyscg-0041: Externalize Configuration and Secrets

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-693 (pillar), CWE-798 (Use of Hard-coded Credentials), CWE-259 (Use of Hard-coded Password), CWE-321 (Use of Hard-coded Cryptographic Key).

## Rule

**Never hard-code** passwords, API keys, tokens, SSH keys, service-account credentials, or IP addresses in source code or deliverable packages. Inject all sensitive configuration at deployment time from protected external files, environment variables, or a secrets manager.

## Why

Hard-coded secrets can be extracted from source, bytecode (`.pyc`/`.pyo`), or compiled packages. They do not scale (every instance shares the same secret), cannot be rotated without a code change, and may expose customer data in violation of HIPAA, GDPR, or CCPA. Bandit rules B105/B106/B107 and CodeQL flag these automatically.

## Non-compliant

```py
def front_end():
    server_config = {}
    server_config["IP"]   = "192.168.0.1"
    server_config["PORT"] = "8080"
    server_config["USER"] = "admin"
    server_config["PASS"] = "SuperSecret123"   # hard-coded credential

    logging.debug("connecting to server PASS %s", server_config["PASS"])
```

The password is baked into the source and printed to logs on every run.

## Compliant

```py
import configparser
from pathlib import Path

def front_end(config_file_path: Path):
    _config = configparser.ConfigParser()
    _config.read(config_file_path)          # config injected by deployment

    logging.debug("connecting to server IP %s",   _config["SERVER"]["IP"])
    logging.debug("connecting to server USER %s", _config["SERVER"]["USER"])
    logging.debug("connecting to server pem %s",  _config["SERVER"]["CERT_FILE"])
    # No password — replaced with certificate-based auth

# Deployment sets file permissions: config_file_path.chmod(0o400)
```

The deployment step owns the config file, sets it read-only to a single OS user, and replaces password-based auth with a certificate.

## Key patterns

| Anti-pattern | Recommended pattern |
|---|---|
| Hard-coded password | Time-limited key/token assigned at deploy time |
| Shared username | RBAC / ABAC / policy engine |
| Hard-coded IP/port | DNS (with DoT/DoQ/DNSSEC) + mTLS |
| Hard-coded UID/GID | Identity names |

Cross-reference: pyscg-0019 (Exclude Sensitive Data From Logs) — do not log connection details in production.
