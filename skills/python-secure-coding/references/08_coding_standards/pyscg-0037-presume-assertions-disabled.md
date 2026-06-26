# pyscg-0037: Presume Assertions May Be Disabled In Production

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-691 (pillar), CWE-617 (Reachable Assertion).

## Rule

Use `assert` only for **internal invariants and debug-only checks** that are not required for correct or safe execution. For security checks, input validation, and any runtime condition that must always be enforced, raise an appropriate exception (`ValueError`, `TypeError`, etc.) instead.

## Why

Running Python with `-O` or `-OO` (or setting `PYTHONOPTIMIZE`) strips all `assert` statements from bytecode and sets `__debug__ = False`. Any security or correctness check implemented solely via `assert` silently disappears in optimized builds, turning a guarded function into an unguarded one.

## Non-compliant

```py
import math

def my_exp(x):
    assert x in range(1, 710), f"Argument {x} is not valid"  # removed by -O
    return math.exp(x)

# python3 -O noncompliant.py  →  my_exp(0) returns 1.0 (no error),
#                                my_exp(710) raises OverflowError (not the expected ValueError)
```

## Compliant

```py
import math

def my_exp(x):
    if x not in range(1, 710):
        raise ValueError(f"Argument {x} is not valid")  # always enforced
    return math.exp(x)

# python3 -O compliant.py  →  same safe behaviour as without -O
```

> Bandit rule B101 (`assert_used`) flags every `assert` in production code automatically.
