# pyscg-0042: Ensure Correct Operator Precedence

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-691 (pillar, Insufficient Control Flow Management), CWE-783 (Operator Precedence Logic Error).

## Rule

Write expressions so that **each statement performs at most one write operation** and precedence is unambiguous. Avoid clever bit-manipulation or compound augmented-assignment tricks; use explicit `if`/`elif` branches instead.

## Why

Python evaluates `**` right-to-left, augmented assignments (`+=`, `|=`) left-to-right, and ordinary expressions left-to-right — mixing these in a single expression, especially when a method with side-effects is called multiple times, produces results that are correct but fragile and nearly impossible to extend safely. The bug class is often invisible to static analysis (Bandit has no checker for it).

## Non-compliant

```python
def label(number: int) -> list[str]:
    key = int(number < 5)              # (1) small
    key |= ((number & 1) ^ 1) << 1    # (2) for even, 0 for odd
    key |= (number < 0) << 2          # (4) negative
    key |= (number > 0) << 3          # (8) positive

    parts = ("big", "small", "even small", "even small",
             "neg", "neg small", "neg even small", "neg even small",
             "big", "big even", "neg big", "neg big even",
             "big", "big even", "neg big", "neg big even")

    permuted = tuple(parts[(i * 5) & 7] for i in range(8))
    idx = (key * 5) & 7
    return permuted[idx].split(" ")
```

Adding a "positive" or "zero" label to this code is extremely error-prone due to the bit-packing and permuted lookup.

## Compliant

```python
def label(number: int) -> list[str]:
    labels = []
    if number < 0:
        labels.append("neg")
    if number % 2 == 0:
        labels.append("even")
    if number < 5:
        labels.append("small")
    if number >= 5:
        labels.append("big")
    return labels
```

Each condition is independent, readable, and trivially extensible. One write per logical step — no operator precedence surprises.
