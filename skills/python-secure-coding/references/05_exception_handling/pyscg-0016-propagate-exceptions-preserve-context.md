# pyscg-0016: Propagate Exceptions and Preserve Context

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-703 (pillar), CWE-396 (Declaration of Catch for Generic Exception), CWE-209 (Error Message Containing Sensitive Information).

## Rule

Never use a bare `except:` clause. Catch the narrowest applicable exception type so that `KeyboardInterrupt` and `SystemExit` can propagate normally. When recovery is impossible, re-raise with `raise ... from original` to preserve context.

## Why

A bare `except:` catches `BaseException`, including `KeyboardInterrupt`, making a process impossible to stop with Ctrl+C. Silently swallowing exceptions hides bugs, produces incomplete logs, and prevents callers from attempting recovery.

## Non-compliant

```py
from time import sleep

def exception_example():
    while True:
        try:
            sleep(1)
            _ = 1 / 0
        except:               # catches KeyboardInterrupt — Ctrl+C has no effect
            print("Don't care")

exception_example()
```

## Compliant

```py
from time import sleep

def exception_example():
    while True:
        sleep(1)
        try:
            _ = 1 / 0
        except ZeroDivisionError:   # specific; KeyboardInterrupt propagates
            print("How is it now?")

exception_example()
```

When re-raising with context:

```py
def slice_cake(cake: int, plates: int) -> float:
    try:
        return cake / plates
    except ZeroDivisionError as zero_division_error:
        raise ZeroDivisionError(
            "slice_cake: You got to give me plates"
        ) from zero_division_error   # preserves original traceback
```

> Detected by: Ruff `E722`, Pylint `W0702`, flake8 `E722`.
