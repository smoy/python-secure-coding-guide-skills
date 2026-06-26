# pyscg-0004: Use Integer Loop Counters

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-197 (Numeric Truncation Error).

## Rule

Use `int` (or `range()`) for loop counters and accumulators. Convert to `float`
only at the point of use. A `float` counter gives unpredictable termination and
can loop forever.

## Why

`float` can't represent most decimal steps exactly: `0.1 + 0.2 == 0.30000000000000004`.
So `counter == 0.8` may never be true, and incrementing by a value too small to
change the mantissa (`1.0 + 1e-16`) never advances — an infinite loop.

## Non-compliant

```py
counter = 0.0
while counter <= 1.0:
    if counter == 0.8:        # never true
        print("reached 0.8")
        break
    counter += 0.1
```

## Compliant

```py
counter = 0
while counter <= 10:
    value = counter / 10      # convert only where needed
    if value == 0.8:
        print("reached 0.8")
        break
    counter += 1
```

Prefer `for i in range(10):` where possible — it's compact and structurally
prohibits a float counter. Relates to
[pyscg-0001](pyscg-0001-control-numeric-precision.md).
