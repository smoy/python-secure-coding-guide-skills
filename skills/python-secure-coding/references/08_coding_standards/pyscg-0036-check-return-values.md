# pyscg-0036: Check Return Values

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-703 (pillar), CWE-252 (Unchecked Return Value).

## Rule

Always capture and inspect return values. For **immutable types** (str, int, tuple), methods that "modify" them return a new object — discard it and the original is unchanged. For functions that signal failure via a sentinel (e.g. `str.find()` returns `-1`), check the sentinel before using the result.

## Why

Ignoring a return value from an immutable-type method silently leaves the original unchanged, causing logic errors that are easy to miss. Ignoring a sentinel such as `-1` from `str.find()` causes it to be used as a valid index (last element), producing incorrect output or unexpected data corruption.

## Non-compliant

```python
# str.replace() returns a new str — ignoring it leaves user_input unchanged
def silly_string(user_input):
    user_input.replace("un", "very ")  # return value discarded
    return user_input                  # still "unsafe string"

# str.find() returns -1 when not found — using it as an index corrupts output
def wrap_in_quotes(full_string, sub_string):
    index_start = full_string.find(sub_string)   # could be -1
    index_end = index_start + len(sub_string)
    return full_string[:index_start] + '"' + full_string[index_start:index_end] + '"' + full_string[index_end:]
```

## Compliant

```python
# Capture the return value of str.replace()
def silly_string(user_input):
    return user_input.replace("un", "very ")   # "very safe string"

# Guard against the -1 sentinel before using the index
def wrap_in_quotes(full_string, sub_string):
    index_start = full_string.find(sub_string)
    if index_start < 0:
        return full_string   # substring not found; return unchanged
    index_end = index_start + len(sub_string)
    return full_string[:index_start] + '"' + full_string[index_start:index_end] + '"' + full_string[index_end:]
```
