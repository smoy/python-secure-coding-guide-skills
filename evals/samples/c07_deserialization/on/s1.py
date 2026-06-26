import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Session:
    user_id: int = 0
    username: str = ""
    roles: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def load_session(data: bytes) -> Session:
    """Reconstruct a Session from JSON bytes received from a client.

    Uses JSON rather than pickle so that no executable opcodes can be
    embedded in the payload.  Each field is explicitly coerced to its
    expected type; unexpected keys are silently ignored, which prevents
    prototype-pollution-style attacks.

    Raises:
        ValueError: if the payload is not valid JSON or is missing
                    required fields.
        TypeError:  if a field value cannot be coerced to the expected type.
    """
    try:
        raw: dict = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid session payload: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Session payload must be a JSON object")

    session = Session()
    session.user_id = int(raw["user_id"])
    session.username = str(raw["username"])

    roles = raw.get("roles", [])
    if not isinstance(roles, list):
        raise ValueError("'roles' must be a JSON array")
    session.roles = [str(r) for r in roles]

    metadata = raw.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("'metadata' must be a JSON object")
    session.metadata = {str(k): v for k, v in metadata.items()}

    return session
