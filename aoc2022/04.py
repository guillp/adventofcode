import re
from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    pairs = [tuple(int(x) for x in re.findall(r"\d+", line)) for line in content.splitlines()]

    yield sum((a <= c and b >= d) or (c <= a and d >= b) for a, b, c, d in pairs)
    yield sum(
        b >= c >= a or (b >= d and a <= c) or b >= d >= a or d >= a >= c or (d >= b and c <= a) or d >= b >= c
        for a, b, c, d in pairs
    )


assert tuple(
    solve("""\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""),
) == (2, 4)


with open("04.txt") as finput:
    content = finput.read()

for part in solve(content):
    print(part)
