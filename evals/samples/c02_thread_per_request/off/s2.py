from concurrent.futures import ThreadPoolExecutor


def process_message(msg):
    return f"processed: {msg}"


class MessageAPI:
    def add_messages(self, messages):
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_message, messages))
        return results
