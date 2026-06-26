# pyscg-0026: Prevent Deadlocks

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-833 (Deadlock).

## Rule

Do not submit **interdependent** tasks to the same bounded `ThreadPoolExecutor`.
If a task running on the pool submits a nested task to the *same* pool and then
blocks on its `.result()`, you can hit a **thread-starvation deadlock**: every
worker is waiting for a queued task that no free worker can ever pick up.

`max_workers` defaults to `min(32, os.cpu_count() + 4)` (Python 3.8+), so the
trap appears once concurrent parent tasks exceed the worker count.

## Non-compliant — nested submit + wait on the same pool

```py
class ReportTableGenerator:
    def __init__(self):
        self.executor = ThreadPoolExecutor()

    def generate(self, inputs):
        futures = [self.executor.submit(self._create_row, i) for i in inputs]
        return "".join(f.result() for f in futures)

    def _create_row(self, row):
        # nested submit to the SAME pool, then block -> can deadlock
        future = self.executor.submit(self._reformat, row)
        return f"|{future.result()}|{len(row)}|\n"
```

## Compliant — don't nest; run the sub-step inline

```py
    def _create_row(self, row):
        return f"|{self._reformat(row)}|{len(row)}|\n"   # no nested submit
```

Options when you genuinely need fork/join:
1. Flatten — call the sub-step directly instead of submitting it (shown above).
2. Use a **separate** executor for the nested level.
3. Emulate Java's `CallerRunsPolicy`: track running tasks and, when the pool is
   near saturation, run the work in the calling thread instead of submitting it.

See [pyscg-0025](pyscg-0025-adequate-resource-pools.md).
