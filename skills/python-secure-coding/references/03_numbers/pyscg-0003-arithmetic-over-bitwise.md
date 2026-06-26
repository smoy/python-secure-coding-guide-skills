# pyscg-0003: Use Arithmetic Over Bitwise Operations

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-1335 (Incorrect Bitwise Shift of Integer).

## Rule

Don't use bit-shifts (`<<`, `>>`) as a stand-in for multiplication/division, and
don't mix bitwise and arithmetic operations on the same data. Use explicit
`*` / `/`. Reserve bitwise ops for genuine bit manipulation (protocols, raw
binary, ctypes/C interop, crypto), and understand the semantics when you must.

## Why

- **Readability / intent**: `x << 2` hides that you meant `x * 4`.
- **Operator precedence bites**: `8 << 2 + 10` parses as `8 << (2 + 10)` →
  `32768`, not `(8 << 2) + 10` → `42`.
- **Sign / truncation surprises**: arithmetic right-shift of a negative truncates
  toward negative infinity. `-50 >> 2` → `-13`, not `-12`. Python stores the sign
  separately, so shifted negatives converge to `-1`, never `0`.
- CPython auto-grows `int` storage, so a runaway shift (`x << 1000000000`) silently
  consumes memory instead of overflowing — a DoS footgun in loops.

## Non-compliant

```py
print(8 << 2 + 10)   # -> 32768, programmer expected 42
foo = -50
foo >>= 2
print(foo)           # -> -13, programmer expected -12
```

## Compliant

```py
print(8 * 4 + 10)    # -> 42, intent is explicit
bar = -50 / 4
print(bar)           # -> -12.5
```

If bit-shifts are unavoidable, parenthesize explicitly and also apply
[pyscg-0002](pyscg-0002-guard-fixed-width-overflow.md) overflow checks at any
C/ctypes boundary.
