# pyscg-0024: Ensure Thread Pool Tasks Can Be Interrupted

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-400 (Uncontrolled Resource Consumption).

## Rule

`Future.cancel()` only stops a task that **hasn't started yet**; on a running
task it returns `False` and does nothing. To make in-flight tasks interruptible
(for graceful shutdown and to bound resource use), have the task periodically
check a shared `threading.Event` and bail out when it's set.

## Non-compliant

```py
from concurrent.futures import ThreadPoolExecutor
import time

def take_time(x):
    for _ in range(10):
        time.sleep(1)        # no way to interrupt mid-run

with ThreadPoolExecutor() as executor:
    future = executor.submit(take_time, "A")
    future.cancel()          # returns False once running; task keeps going
```

## Compliant

```py
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import time

def take_time(x, event: Event):
    for _ in range(10):
        if event.is_set():
            return            # cooperative interruption (save partial work here)
        time.sleep(1)

with ThreadPoolExecutor() as executor:
    event = Event()
    future = executor.submit(take_time, "A", event)
    future.cancel()           # in case it hasn't started
    event.set()               # signal a running task to stop
```

The task must *cooperate* by checking the flag at safe points; there is no forced
thread kill in Python. Pair with [pyscg-0025](pyscg-0025-adequate-resource-pools.md).
