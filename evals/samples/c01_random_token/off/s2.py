import uuid
import hashlib
import time


def make_reset_token():
    raw = f"{uuid.uuid4()}-{time.time()}"
    token = hashlib.md5(raw.encode()).hexdigest()
    return token


if __name__ == '__main__':
    print(make_reset_token())
