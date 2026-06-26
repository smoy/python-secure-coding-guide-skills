import threading


def process_message(msg):
    return f"processed: {msg}"


class MessageAPI:
    def add_messages(self, messages):
        results = [None] * len(messages)
        threads = []

        def worker(index, msg):
            results[index] = process_message(msg)

        for i, msg in enumerate(messages):
            t = threading.Thread(target=worker, args=(i, msg))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return results
