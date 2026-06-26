import os
import subprocess


def list_dir(name):
    result = subprocess.run(
        f"ls {name}",
        shell=True,
        capture_output=True,
        text=True,
    )
    files = result.stdout.strip().splitlines()
    return files
