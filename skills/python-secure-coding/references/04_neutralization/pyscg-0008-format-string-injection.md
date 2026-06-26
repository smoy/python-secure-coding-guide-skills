# pyscg-0008: Prevent Format String Injection

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-134 (Use of Externally-Controlled Format String).

*Overlaps the security-guidance plugin (the reactive/detective layer); this is the proactive Python-idiom complement.*

## Rule

Never pass a format string that is assembled from user input. Use `string.Template` with fixed templates, or f-strings with explicit, controlled substitution keys — not `str.format()` on a string built by concatenating user data.

## Why

Python's `str.format()` lets callers traverse object graphs via attribute access (`{0.__init__.__globals__[SECRET]}`). If user input becomes part of the format template, any global variable reachable from objects passed to `format()` can be exfiltrated — including secrets. `string.Template` restricts substitution to named `$key` placeholders and does not expose attribute traversal.

## Non-compliant

```python
import sys

ENCRYPTION_KEY = "FL4G1"
MESSAGE = "Contract '{0.instance_name}' created for "

class MicroService:
    def __init__(self, instance_name):
        self.instance_name = instance_name

def front_end(customer):
    message_format = MESSAGE + customer          # user data enters the template
    mc = MicroService("big time microservice")
    print(message_format.format(mc))             # exposes __globals__

# Attacker passes: "{0.__init__.__globals__[ENCRYPTION_KEY]}"
front_end("{0.__init__.__globals__[ENCRYPTION_KEY]}")
```

## Compliant

```python
import sys
from string import Template

ENCRYPTION_KEY = "FL4G1"
MESSAGE = Template("Contract '$instance_name' created for '$customer'")

class MicroService:
    def __init__(self, instance_name):
        self.instance_name = instance_name

    def get_instance_name(self) -> str:
        return self.instance_name

def front_end(customer):
    mc = MicroService("big time microservice")
    print(MESSAGE.substitute(instance_name=mc.get_instance_name(),
                             customer=customer))  # no traversal possible
```

`string.Template` with keyword substitution prevents attribute-path traversal and keeps sensitive globals unexposed regardless of what `customer` contains.
