from collections.abc import Iterator
from functools import cache


@cache
def blink(stone: int, n: int) -> Iterator[int]:
    if n == 0:
        return (stone,)

    match stone:
        case 0:
            return blink(1, n - 1)
        case _ if (l := len(s := str(stone))) % 2 == 0:
            return (*blink(int(s[: l // 2]), n - 1), *blink(int(s[l // 2 :]), n - 1))
        case _:
            return blink(stone * 2024, n - 1)


def solve(content: str) -> Iterator[int]:
    stones = tuple(map(int, content.strip().split()))

    part1 = []
    for stone in stones:
        part1.extend(blink(stone, 25))
    yield len(part1)

    intermediate = []
    for stone in part1:
        intermediate.extend(blink(stone, 25))

    part2 = []
    for stone in intermediate:
        part2.extend(blink(stone, 25))
    yield len(part2)


assert next(solve("125 17")) == 55312

with open("11.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
