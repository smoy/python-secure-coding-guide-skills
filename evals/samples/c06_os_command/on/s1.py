import os
from pathlib import Path


def list_dir(name: str) -> list[str]:
    allowed_root = Path.home()
    target = allowed_root.joinpath(name).resolve()
    target.relative_to(allowed_root.resolve())  # raises ValueError on traversal
    return [entry.name for entry in target.iterdir()]
