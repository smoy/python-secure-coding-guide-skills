import hashlib
import hmac
import os
import pickle
from dataclasses import dataclass, field
from typing import Any


# In production, load this from a secrets manager or environment variable.
# Never hard-code the key in source.
_SESSION_HMAC_KEY: bytes = os.environb.get(b"SESSION_HMAC_KEY", b"")


@dataclass
class Session:
    user_id: int = 0
    username: str = ""
    roles: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def load_session(data: bytes) -> Session:
    """Reconstruct a Session from a signed pickle payload received from a client.

    The wire format is:  <64-hex-char HMAC-SHA256 digest> + b":" + <pickle bytes>

    The HMAC digest is computed over the raw pickle bytes using a server-side
    secret key.  The signature is verified with hmac.compare_digest (constant-
    time comparison) before pickle.loads() is ever called.  If the signature
    does not match, the payload is rejected without any deserialization.

    This pattern follows pyscg-0023: when pickle is architecturally unavoidable,
    guard it with an HMAC integrity check so that attacker-crafted opcodes are
    rejected before execution.

    Raises:
        EnvironmentError: if the HMAC key has not been configured.
        ValueError:        if the payload is malformed or the signature is invalid.
    """
    if not _SESSION_HMAC_KEY:
        raise EnvironmentError(
            "SESSION_HMAC_KEY environment variable is not set; "
            "cannot verify session integrity."
        )

    # Split on the first colon only so that the pickle bytes may contain colons.
    try:
        digest_hex, pickle_bytes = data.split(b":", 1)
    except ValueError:
        raise ValueError("Malformed session payload: expected <digest>:<pickle>")

    expected_digest = hmac.new(
        _SESSION_HMAC_KEY, pickle_bytes, hashlib.sha256
    ).hexdigest().encode()

    if not hmac.compare_digest(digest_hex, expected_digest):
        raise ValueError("Session payload signature verification failed")

    # Safe: pickle.loads() is called only after the HMAC-SHA256 signature above
    # has been verified with a constant-time comparison.  Any attacker-controlled
    # bytes will fail the integrity check before this line is reached.
    obj = pickle.loads(pickle_bytes)

    if not isinstance(obj, Session):
        raise TypeError(
            f"Deserialized object is {type(obj).__name__!r}, expected 'Session'"
        )

    return obj


def dump_session(session: Session) -> bytes:
    """Serialize a Session to a signed pickle payload (server-side helper)."""
    if not _SESSION_HMAC_KEY:
        raise EnvironmentError(
            "SESSION_HMAC_KEY environment variable is not set"
        )

    pickle_bytes = pickle.dumps(session)
    digest = hmac.new(
        _SESSION_HMAC_KEY, pickle_bytes, hashlib.sha256
    ).hexdigest().encode()
    return digest + b":" + pickle_bytes
