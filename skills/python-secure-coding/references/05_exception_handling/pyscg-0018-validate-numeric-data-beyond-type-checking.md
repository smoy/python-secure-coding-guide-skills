# pyscg-0018: Validate Numeric Data Beyond Type Checking

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-703 (pillar), CWE-754 (Improper Check for Unusual or Exceptional Conditions), CWE-230 (Improper Handling of Missing Values).

## Rule

After converting input to `float`, explicitly check for `NaN` and infinite values using `math.isnan()` and `math.isfinite()`. Never use `== float("NaN")` or `is float("NaN")` — those comparisons always return `False` (IEEE 754 behavior).

## Why

`float()` accepts `"NaN"`, `"inf"`, and `"-infinity"` as valid inputs. `NaN` propagates silently through arithmetic and comparisons (including `NaN == NaN` → `False`), corrupting results without raising an exception. Infinity bypasses range guards.

## Non-compliant

```py
def add_to_package(self, object_weight: str):
    value = float(object_weight)
    if value == "NaN":            # dead code — float never equals string
        raise ValueError("'NaN' not a number")
    if isinstance(value, float) is False:  # also dead code after float()
        raise ValueError("not a number")
    if self.package_weight + value > self.max_package_weight:
        raise ValueError("Addition would exceed maximum package weight.")
    self.package_weight += value  # corrupted by NaN or infinity inputs
```

## Compliant

```py
import math

def add_to_package(self, object_weight) -> None:
    try:
        value = float(object_weight)
    except (ValueError, TypeError) as e:
        raise ValueError("Input cannot be converted to a float.") from e
    if math.isnan(value):
        raise ValueError("Input is not a number.")
    if not math.isfinite(value):
        raise ValueError("Input is not a finite number.")
    if value < 0:
        raise ValueError("Weight must be a non-negative number.")
    if self.package_weight + value > self.max_package_weight:
        raise ValueError("Addition would exceed maximum package weight.")
    self.package_weight += value
```

> Alternative: use `decimal.Decimal` for currency/precision use cases — it raises `decimal.InvalidOperation` on `NaN` automatically.
