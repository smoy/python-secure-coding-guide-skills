# pyscg-0031: Use Copies When Modifying Iterables

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-710 (pillar), CWE-1095 (Loop Condition Value Update within the Loop).

## Rule

Never add, remove, or replace elements of a `list`, `dict`, or `set` while iterating over it directly. Instead, iterate over a **copy** (`collection.copy()`) or build a **new collection**, then modify the original outside the loop.

## Why

Mutating a list during iteration silently skips elements (the iterator sees shifted indices). Mutating a dict or set raises `RuntimeError: dictionary/set changed size during iteration`. Both outcomes are unpredictable and can lead to logic errors or denial of service.

## Non-compliant

```py
# list: silently skips 'Bill' — only one 'B' name is removed
userlist = ['Alice', 'Bob', 'Bill', 'Charlie']
for user in userlist:
    if user.startswith('B'):
        userlist.remove(user)  # shifts indices; iterator skips next element

# dict: raises RuntimeError
userdict = {'Alice': 'active', 'Bob': 'inactive', 'Charlie': 'active'}
for user, status in userdict.items():
    if status == 'inactive':
        del userdict[user]  # RuntimeError: dictionary changed size during iteration
```

## Compliant

```py
# Iterate over a copy, modify the original
userlist = ['Alice', 'Bob', 'Bill', 'Charlie']
for user in userlist.copy():
    if user.startswith('B'):
        userlist.remove(user)

# Dict: copy().items() so the original can be safely modified
userdict = {'Alice': 'active', 'Bob': 'inactive', 'Charlie': 'active'}
for user, status in userdict.copy().items():
    if status == 'inactive':
        del userdict[user]

# Alternative: build a new collection
activeusers = [u for u in userlist if not u.startswith('B')]
```

> Use `copy.deepcopy()` instead of `.copy()` when nested mutable objects must also be independent.
