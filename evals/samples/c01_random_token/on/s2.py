import os
import hashlib


def make_reset_token() -> str:
    """Return a hex-encoded, cryptographically random token for password-reset emails.

    Reads 32 bytes directly from os.urandom (the OS CSPRNG), then hex-encodes them
    to produce a 64-character lowercase hex string.  os.urandom is the underlying
    source that the secrets module also uses, so this satisfies pyscg-0038.
    The random module is deliberately avoided; it is a deterministic PRNG whose
    state can be reconstructed by an attacker.
    """
    return os.urandom(32).hex()
