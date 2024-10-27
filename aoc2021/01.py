from collections.abc import Iterator
from itertools import pairwise


def solve(content: str) -> Iterator[int]:
    depths = tuple(int(x) for x in content.splitlines())
    yield sum(b > a for a, b in pairwise(depths))
    yield sum(b + c + d > a + b + c for a, b, c, d in zip(depths, depths[1:], depths[2:], depths[3:]))


assert tuple(
    solve("""\
199
200
208
210
200
207
240
269
260
263
"""),
) == (7, 5)

with open("01.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
