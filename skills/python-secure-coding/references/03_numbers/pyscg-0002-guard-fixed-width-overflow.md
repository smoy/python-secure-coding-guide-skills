# pyscg-0002: Guard Fixed-Width Numbers Against Overflow

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-190 (Integer Overflow or Wraparound), CWE-191 (Integer Underflow), CWE-682.

## Rule

Python's built-in `int` is arbitrary-precision and won't overflow. But
**fixed-width / C-backed numerics will**, and they appear whenever Python crosses
into C: `numpy`/`ctypes` integer types, `datetime`/`timedelta` (libpython C limits),
and C-implemented math like `math.exp`. When using these, detect and handle
overflow (boundary checks and/or catching the exception).

## Failure modes

- `numpy.int64` **wraps silently** past its max (sign flips), often only a
  `RuntimeWarning`; constructing from a too-large Python int raises `OverflowError`.
- `datetime`/`timedelta` is bounded to years 1–9999 → `OverflowError` /
  `date value out of range` for large offsets.
- `math.exp(1000)` → `OverflowError: math range error`.

## Non-compliant

```py
import numpy
a = numpy.int64(numpy.iinfo(numpy.int64).max)
print(a + 1)   # RuntimeWarning, wraps to -9223372036854775808
```

## Compliant — promote warnings and catch

```py
import warnings, numpy
a = numpy.int64(numpy.iinfo(numpy.int64).max)
with warnings.catch_warnings():           # scope the filter; don't change it globally
    warnings.filterwarnings("error")      # turn the RuntimeWarning into an exception
    try:
        print(a + 1)
    except Warning:
        print("overflow detected")
```

## Compliant — bound inputs before crossing into C

```py
from datetime import datetime, timedelta

def get_datetime(currtime: datetime, hours: int) -> datetime:
    hours_min = (currtime - datetime(1, 1, 1)).total_seconds() // 3600 * -1
    hours_max = (datetime(9999, 12, 31) - currtime).total_seconds() // 3600
    if not (hours_min <= hours <= hours_max):
        raise ValueError("hours out of range")
    return currtime + timedelta(hours=hours)
```

For `math.exp` and similar, wrap the call in `try/except OverflowError`. Always
validate attacker-influenced sizes *before* handing them to a C boundary.
