import hashlib
from collections.abc import Iterator


def md5hash(secret: bytes, i: int) -> str:
    return hashlib.md5(secret + str(i).encode()).hexdigest()


def solve(content: str) -> Iterator[int]:
    secret = content.encode()

    i = 0
    while not md5hash(secret, i).startswith("0" * 5):
        i += 1
    yield i

    while not md5hash(secret, i).startswith("0" * 6):
        i += 1

    yield i


secret = "ckczppom"

for part in solve(secret):
    print(part)
