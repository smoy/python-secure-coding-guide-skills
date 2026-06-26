import os
from pathlib import Path


def list_dir(name: str) -> list[str]:
    allowed_root = Path("/tmp/sandbox").resolve()
    target = (allowed_root / name).resolve()
    if not str(target).startswith(str(allowed_root)):
        raise ValueError(f"Directory {name!r} is outside the allowed root")
    return os.listdir(target)
