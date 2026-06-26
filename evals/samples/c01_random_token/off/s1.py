import random
import string
import time


def make_reset_token(length=32):
    random.seed(time.time())
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


if __name__ == '__main__':
    print(make_reset_token())
