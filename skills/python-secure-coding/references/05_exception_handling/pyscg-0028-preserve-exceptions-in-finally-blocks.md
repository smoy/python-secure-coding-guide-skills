# pyscg-0028: Preserve Exceptions in Finally Blocks

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-459 (Incomplete Cleanup), CWE-584 (Return Inside Finally Block).

## Rule

Never place `return`, `break`, or `continue` statements **inside** a `finally` block. Per the Python language specification, any such statement discards the in-flight exception, silently swallowing it.

## Why

A `return` inside `finally` causes the function to return normally even when an exception was raised in the `try` block. The exception is lost — callers cannot detect or recover from the failure.

## Non-compliant

```py
def do_logic():
    try:
        raise Exception
    finally:
        print("logic done")
        return True   # swallows the exception; caller sees True, not an error

do_logic()            # prints "logic done", no exception propagates
```

## Compliant

```py
def do_logic():
    try:
        raise Exception
    finally:
        print("logic done")   # cleanup only — no return/break/continue
    # return belongs here, outside the finally block
    return True

do_logic()                    # exception propagates correctly
```

> Detected by: Pylint `W0150` (lost-exception), Pylint `W0134` (return shadowed by finally).
