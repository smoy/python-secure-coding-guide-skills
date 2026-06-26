# pyscg-0011: Prevent Type Confusion

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-843 (Access of Resource Using Incompatible Type / 'Type Confusion').

## Rule

Never rely solely on type hints for runtime type safety. Explicitly cast or validate external values to the expected type before operating on them, especially when interoperating with C/C++ binary data (`struct`, `ctypes`) or accepting input from an untrusted caller.

## Why

Python type hints are a design-time aid only — they are not enforced at runtime. An attacker (or a bug) that passes a `str` where an `int` is expected can cause unexpected behavior: `int(100) * str("3")` repeats the string 100 times instead of multiplying. In binary interop scenarios, a mismatched endianness or signedness (e.g., reading a little-endian value with a big-endian format code) silently produces a wrong numeric result that can corrupt downstream logic or cause integer-range confusion.

## Non-compliant

```python
def shopping_bag(price: int, qty: int) -> int:
    return price * qty          # type hint not enforced at runtime

# Attacker/bug passes a string:
print(shopping_bag(100, "3"))   # prints "3" repeated 100 times, not 300
```

## Compliant

```python
def shopping_bag(price: int, qty: int) -> int:
    return int(price) * int(qty)   # explicit cast enforces numeric semantics

print(shopping_bag(100, "3"))      # raises ValueError if "3" is non-numeric,
                                   # or correctly returns 300
```

For stricter enforcement, raise a `TypeError` or `ValueError` explicitly when the input cannot be converted, rather than silently coercing. When using `struct.unpack` on external binary data, verify byte order and signedness against the documented wire format.
