import hashlib
import re
from collections.abc import Iterator
from functools import lru_cache
from itertools import count

test_content = b"abc"
content = b"yjdafjpo"


@lru_cache(1000)
def md5hash(content: bytes, i: int, *, part2: bool = False) -> str:
    h = hashlib.md5(content)
    h.update(str(i).encode())
    if part2:
        for _ in range(2016):
            h = hashlib.md5(h.hexdigest().encode())
    return h.hexdigest()


def find_keys(content: bytes, *, part2: bool = False) -> Iterator[int]:
    for i in count():
        h = md5hash(content, i, part2=part2)
        for c in re.findall(r"(.)\1\1\1\1", h):
            for j in range(max(0, i - 1000), i):
                m = re.findall(r"(.)\1\1", md5hash(content, j, part2=part2))
                if m and m[0] == c:
                    yield j


def solve(content: bytes, n: int = 64, *, part2: bool = False) -> int:
    s: list[int] = []
    iterator = find_keys(content, part2=part2)
    while len(s) <= n or s[n] > max(s) - 1000:
        i = next(iterator)
        s.append(i)
        s.sort()
    return s[n - 1]


assert md5hash(test_content, 0, part2=True) == "a107ff634856bb300138cac6568c0f24"

assert solve(test_content) == 22728
assert solve(test_content, part2=True) == 22551

print(solve(content))
print(solve(content, part2=True))
