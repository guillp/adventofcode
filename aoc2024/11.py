from collections.abc import Iterator
from functools import cache


def blink(stone: int) -> tuple[int, ...]:
    match stone:
        case 0:
            return (1,)
        case _ if (l := len(s := str(stone))) % 2 == 0:
            return int(s[: l // 2]), int(s[l // 2 :])
        case _:
            return (stone * 2024,)


@cache
def cached_blink(stone: int, n: int) -> int:
    if n == 0:
        return 1
    return sum(cached_blink(b, n - 1) for b in blink(stone))


def solve(content: str) -> Iterator[int]:
    stones = tuple(map(int, content.strip().split()))

    yield sum(cached_blink(stone, 25) for stone in stones)
    yield sum(cached_blink(stone, 75) for stone in stones)


assert next(solve("125 17")) == 55312

with open("11.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
