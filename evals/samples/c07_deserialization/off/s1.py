import pickle


def load_session(data: bytes) -> object:
    """Reconstruct a session object from bytes received from a client."""
    session = pickle.loads(data)
    return session
