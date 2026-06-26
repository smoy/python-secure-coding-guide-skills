# pyscg-0052: Ensure Cleanup on Exceptions

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-460 (Improper Cleanup on Thrown Exception).

## Rule

Use the `with` statement (context manager) for any resource that must be released — locks, files, sockets, database connections — so that cleanup runs automatically even when an exception is raised.

## Why

If an exception fires before an explicit `resource.release()` call, the release is skipped and the resource remains held (e.g., a lock that is never released causes a deadlock). Context managers guarantee the `__exit__` path runs regardless of how the block exits.

## Non-compliant

```py
import threading

lock = threading.Lock()

def perform_critical_operation():
    lock.acquire()
    print("Lock acquired, performing critical operation...")
    raise ValueError("Something went wrong!")
    lock.release()   # never reached — lock stays acquired

try:
    perform_critical_operation()
except ValueError as e:
    print(f"Caught exception: {e}")

lock.acquire()       # deadlock: lock was never released
```

## Compliant

```py
import threading

lock = threading.Lock()

def perform_critical_operation():
    with lock:   # automatically released on exit, including exceptions
        print("Lock acquired, performing critical operation...")
        raise ValueError("Something went wrong!")

try:
    perform_critical_operation()
except ValueError as e:
    print(f"Caught exception: {e}")
# lock is released; subsequent acquire succeeds
```

> See also: pyscg-0028 (preserve exceptions in finally blocks), pyscg-0015 (handle error conditions).
