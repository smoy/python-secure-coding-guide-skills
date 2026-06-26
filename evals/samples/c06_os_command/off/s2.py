import os


def list_dir(name):
    command = "ls " + name
    output = os.popen(command).read()
    files = output.strip().splitlines()
    return files
