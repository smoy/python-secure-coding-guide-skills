# pyscg-0034: Check for None Values

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-703 (pillar), CWE-476 (NULL Pointer Dereference).

## Rule

Before calling methods on, accessing fields of, or calling `len()` on any object that may be `None`, **guard with an explicit `None` check** (`if x is None`). Never `raise None`; raise a proper exception class instead.

## Why

Calling `.split()`, `len()`, or any attribute on `None` raises `AttributeError` or `TypeError`, which can crash the application (denial of service). Data from external or lesser-trusted sources must be validated before use; even trusted sources can return `None` legitimately. Raising `None` instead of an exception class produces an unhelpful `TypeError: exceptions must derive from BaseException` with no diagnostic information.

## Non-compliant

```py
def is_valid_name(s: str) -> bool:
    names = s.split()          # AttributeError if s is None
    if len(names) != 2:
        return False
    return s.istitle()

def print_number_of_students(classroom: list[str]):
    print(f"The classroom has {len(classroom)} students.")  # TypeError if None

def check_list(classroom: list[str]):
    if not isinstance(classroom, list):
        raise None             # TypeError: exceptions must derive from BaseException
```

## Compliant

```py
from typing import Optional

def is_valid_name(s: Optional[str]) -> bool:
    if s is None:
        return False
    names = s.split()
    if len(names) != 2:
        return False
    return s.istitle()

def print_number_of_students(classroom: list[str]):
    if isinstance(classroom, list):
        print(f"The classroom has {len(classroom)} students.")
    else:
        print("Given object is not a classroom.")

def check_list(classroom: list[str]):
    if not isinstance(classroom, list):
        raise ValueError("classroom is not a list")
```

> Static type checkers (mypy, pyright, pylance) flag `None`-passing and `raise None` at analysis time.
