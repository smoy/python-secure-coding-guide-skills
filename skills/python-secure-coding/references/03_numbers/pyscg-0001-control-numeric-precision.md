# pyscg-0001: Control Numeric Precision

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-682 (Incorrect Calculation), CWE-1339 (Insufficient Precision/Accuracy of a Real Number).

## Rule

For values that require exact accuracy (money, banking, billing, measurements,
anything later compared for equality), **do not use `float`**. Use integers (e.g.
whole cents) or `decimal.Decimal`.

## Why

A Python `float` (IEEE-754 double) has only ~15–17 *significant* decimal digits
*total* — shared across digits before and after the point — and cannot exactly
represent many terminating base-10 decimals like `0.33`. As the integer part
grows, fractional precision is lost.

## Non-compliant

```py
BALANCE = 3.00
ITEM_COST = 0.33
ITEM_COUNT = 5
print(BALANCE - ITEM_COUNT * ITEM_COST)
# -> 1.3499999999999999  (expected 1.35)
```

## Compliant — integers (cents)

```py
BALANCE = 300       # cents
ITEM_COST = 33      # cents
ITEM_COUNT = 5
print((BALANCE - ITEM_COUNT * ITEM_COST) / 100)   # -> 1.35
```

## Compliant — Decimal

```py
from decimal import Decimal
BALANCE = Decimal("3.00")
ITEM_COST = Decimal("0.33")
ITEM_COUNT = 5
print(BALANCE - ITEM_COUNT * ITEM_COST)           # -> 1.35
```

Note: construct `Decimal` from **strings** (`Decimal("0.33")`), not floats, or you
re-import the float's imprecision. `Decimal` is slower than native types — use it
where accuracy matters, not in hot loops that don't need it.

Related: [pyscg-0004](pyscg-0004-integer-loop-counters.md) (float loop counters).
