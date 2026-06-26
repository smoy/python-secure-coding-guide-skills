from concurrent.futures import ThreadPoolExecutor, wait


def process_message(msg):
    return msg


class MessageAPI:
    def __init__(self, max_workers: int = 8, timeout: float = 1.0):
        # Explicitly bounded pool — never leave max_workers unset so a burst of
        # incoming messages cannot spawn unbounded threads (CWE-410).
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.timeout = timeout

    def add_messages(self, messages: list) -> list:
        futures = [self.executor.submit(process_message, m) for m in messages]
        done, not_done = wait(futures, timeout=self.timeout)
        for f in not_done:
            f.cancel()
        return [f.result() for f in done]
