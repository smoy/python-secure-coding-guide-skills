# pyscg-0033: Implement Comparisons by Value Rather Than Reference

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-697 (pillar), CWE-595 (Comparison of Object References Instead of Object Contents).

## Rule

For **custom classes**, always implement `__eq__` to compare by value. Use `==` (value equality) for business logic comparisons; reserve `is` exclusively for identity checks (e.g. `x is None`).

## Why

Without `__eq__`, Python's `==` falls back to `id(obj1) == id(obj2)` (reference equality). Two separate instances with identical data compare as unequal, breaking `==`, list equality, and `in` membership tests. Python also caches small integers (−5 to 256) and interns short strings, so `is` may return `True` or `False` unpredictably depending on context, CPython version, or whether code runs in a script vs. REPL.

## Non-compliant

```py
class Integer:
    def __init__(self, value):
        self.value = value

# All three print False — no __eq__, so == compares object identity
print(Integer(12) == Integer(12))           # False
print([Integer(12)] == [Integer(12)])       # False
print(Integer(12) in [Integer(10), Integer(12)])  # False
```

## Compliant

```py
class Integer:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return False

# All three now print True
print(Integer(12) == Integer(12))           # True
print([Integer(12)] == [Integer(12)])       # True
print(Integer(12) in [Integer(10), Integer(12)])  # True
print(Integer(12) == 12)                    # True (int interop)

# 'is' still checks identity — use only for None checks
a = Integer(12)
b = Integer(12)
print(a is b)   # False — different objects, as expected
```

> `dataclasses.dataclass` generates `__eq__` automatically when `eq=True` (the default).
