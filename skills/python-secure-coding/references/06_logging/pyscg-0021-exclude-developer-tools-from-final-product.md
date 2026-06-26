# pyscg-0021: Exclude Developer Tools From the Final Product

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-710 (pillar), CWE-489 (Active Debug Code).

> *Upstream states this rule with anti-pattern/CVE lists and no code examples; the
> Flask snippets below are an illustrative example, not a verbatim port.*

## Rule

Do not ship debug modes, open diagnostic ports, verbose logging, or internal shell-access endpoints in production builds. Keep design tooling (functional tests, performance tests, debuggers) in separate packages that are never installed in the production environment.

## Why

Active debug code in production widens the attack surface. Real CVEs include CVE-2018-14649 (ceph-isci-cli shipped Flask in debug mode, enabling unauthenticated RCE) and CVE-2015-5306 (OpenStack ironic exposed the Flask interactive console when debug was on). Operators who need troubleshooting access in production often indicate that logging is insufficiently designed — fix the logging rather than shipping debug tools.

## Anti-patterns to avoid

- `debug=True` in Flask/Django in production
- Ports left open (e.g. SSH port 22, debugpy port 5678)
- Verbose/DEBUG-level logging enabled on live deployments
- Monkey-patching for in-production tracing
- Hidden endpoints that enable/disable verbose output or spawn a shell
- Test code and fixtures bundled into the production package

## Non-compliant

```python
# Flask app shipped to production with debug mode on
from flask import Flask
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)  # exposes interactive debugger console to attackers
```

## Compliant

```python
import os
from flask import Flask
app = Flask(__name__)

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    # Deployment tooling (not code) controls FLASK_DEBUG; never true in production
    app.run(debug=debug)
```

> See also: pyscg-0019 (exclude sensitive data from logs), pyscg-0020 (informative event logging).
