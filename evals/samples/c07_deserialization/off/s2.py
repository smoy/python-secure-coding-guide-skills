import yaml


def load_session(data: bytes) -> object:
    """Reconstruct a session object from bytes received from a client."""
    session = yaml.load(data, Loader=yaml.Loader)
    return session
