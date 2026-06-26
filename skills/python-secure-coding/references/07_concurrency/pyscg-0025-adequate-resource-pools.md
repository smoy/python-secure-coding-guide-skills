# pyscg-0025: Configure Adequate Resource Pools

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-410 (Insufficient Resource Pool).

## Rule

Don't spawn one thread per request/message (the "thread-per-message" pattern).
Use a **bounded** thread pool with a fixed `max_workers` so a burst of work — or
an attacker flooding the endpoint — can't exhaust CPU/memory. Add timeouts and
input limits at the queue.

## Why

Thread-per-message lets a single caller create unbounded threads and drive CPU
well past 100% across cores, a trivial DoS. A pool caps concurrent workers,
reuses threads, and contains failures.

## Non-compliant — thread per message

```py
import threading

def add_messages(self, messages: list) -> list:
    threads = []
    for message in messages:                 # 1000 messages -> 1000 threads
        t = threading.Thread(target=process_message, args=[message, out])
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
```

## Compliant — bounded pool, with timeout + cancellation

The bounded pool is only half the fix: upstream's compliant solution also bounds
*time* with `wait(..., timeout=...)` and cancels whatever didn't finish, so slow
or hostile tasks can't pin workers indefinitely.

```py
from concurrent.futures import ThreadPoolExecutor, wait

class MessageAPI:
    def __init__(self):
        self.timeout = 1                  # provided by the mediation layer, not hardcoded
        # Default max_workers since Py3.8 is min(32, os.cpu_count()+4); set explicitly
        # to what the downstream layer can sustain. Never leave concurrency unbounded.
        self.executor = ThreadPoolExecutor(max_workers=8)

    def add_messages(self, messages: list) -> list:
        # TODO: also cap len(messages) and sanitize input at the boundary.
        futures = [self.executor.submit(process_message, m) for m in messages]
        done, not_done = wait(futures, timeout=self.timeout)
        for future in not_done:
            future.cancel()               # stop tasks that blew the time budget
        return [f.result() for f in done]
```

A pool alone doesn't stop an attacker creating many pools — front it with rate
limiting / intrusion detection in real deployments. See
[pyscg-0024](pyscg-0024-interruptible-thread-pool-tasks.md) and
[pyscg-0026](pyscg-0026-prevent-deadlocks.md).
