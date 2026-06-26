# pyscg-0014: Use Specific Exception Types

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-703 (pillar), CWE-397 (Declaration of Throws for Generic Exception).

## Rule

Raise and catch **specific exception types**, never the bare `Exception` or `BaseException`. Use a built-in exception that accurately describes the error condition; create a custom subclass only when no built-in fits.

## Why

Raising a generic `Exception` bypasses caller `except` clauses that target the expected specific type, hiding bugs and preventing recovery. `BaseException` is even more dangerous because it also swallows `KeyboardInterrupt` and `SystemExit`.

## Non-compliant

```py
def divide(divided: int, divisor: int) -> float:
    if divisor == 0:
        raise Exception("Cannot divide by zero")  # too generic
    return divided / divisor

try:
    divide(1, 0)
except ZeroDivisionError:
    print("I divided by zero!")   # never reached
except Exception:
    print("Something went wrong and I have no clue what!")
```

## Compliant

```py
def divide(divided: int, divisor: int) -> float:
    if divisor == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return divided / divisor

try:
    divide(1, 0)
except ZeroDivisionError:
    print("I divided by zero!")   # reached correctly
except Exception:
    print("Something went wrong and I have no clue what!")
```
