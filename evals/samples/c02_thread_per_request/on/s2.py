import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_message(msg):
    return msg


_MAX_BATCH = 500
_WORKER_CAP = min(32, (os.cpu_count() or 1) + 4)
_TASK_TIMEOUT = 2.0


class MessageAPI:
    """
    Processes messages concurrently using a shared, bounded thread pool.

    Using a fixed max_workers cap prevents unbounded thread creation that would
    allow a burst of requests to exhaust system resources (CWE-410).
    """

    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=_WORKER_CAP)

    def add_messages(self, messages: list) -> list:
        if len(messages) > _MAX_BATCH:
            raise ValueError(f"Batch size exceeds limit of {_MAX_BATCH}")

        futures = {self._executor.submit(process_message, m): m for m in messages}
        results = []
        for future in as_completed(futures, timeout=_TASK_TIMEOUT):
            results.append(future.result())
        return results

    def shutdown(self, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait)
