# pyscg-0032: Avoid Redefining Built-in Functions or Standard Library Identifiers

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-710 (pillar), CWE-1109 (Use of Same Variable for Multiple Purposes).

## Rule

Do not name your variables, functions, or classes after Python built-ins (e.g. `len`, `list`, `id`) or standard-library modules/classes (e.g. `os`, `str`, `json`). Use a distinct, descriptive name instead (e.g. `custom_len`, `custom_os`).

## Why

Redefining a built-in or standard-library identifier silently shadows the original for the rest of the scope. Callers that expect the real `len()` or `os.getpid()` get the replacement instead, producing wrong results, `TypeError`, or complete loss of functionality. The problem compounds when the redefinition is at module level or made global.

## Non-compliant

```python
# Shadows built-in len(); now len([1,2,3]) returns 6 (sum) instead of 3
def len(numbers: list[int]) -> int:
    result = 0
    for number in numbers:
        result += number
    return result

# Shadows standard-library module os; os.getpid() returns "Not implemented"
import os
print(os.getpid())   # real PID

class os:
    @staticmethod
    def getpid():
        return "Not implemented"

print(os.getpid())   # "Not implemented"
```

## Compliant

```python
def custom_len(numbers: list[int]) -> int:
    result = 0
    for number in numbers:
        result += number
    return result

import os
print(os.getpid())   # always the real PID

class custom_os:
    @staticmethod
    def getpid():
        return "Not implemented"

print(os.getpid())   # still the real PID
```

> Pylint W0622 (`redefined-builtin`) and E0102 (`function-redefined`) flag both patterns automatically.
