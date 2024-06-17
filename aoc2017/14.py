from collections import deque
from itertools import accumulate
from operator import xor


def knothash(content: str, nb: int = 256, rounds: int = 64) -> str:
    numbers = deque(range(nb))
    skip_size = 0
    lengths = [ord(x) for x in content.strip()] + [17, 31, 73, 47, 23]

    for _ in range(rounds):
        for length in lengths:
            numbers = deque(list(reversed([numbers.popleft() for _ in range(length)])) + list(numbers))
            numbers.rotate(-length - skip_size)
            skip_size += 1

    numbers.rotate(sum(lengths) * rounds + sum(range(skip_size)))
    numbers_lst = list(numbers)

    return "".join(f"{tuple(accumulate(numbers_lst[i*16:(i+1)*16], xor))[-1]:02x}" for i in range(16))


def part1(content: str) -> int:
    return sum(f"{int(knothash(f'{content}-{n}'), 16):b}".count("1") for n in range(128))


def part2(content: str) -> int:
    grid = {(x, y) for y in range(128) for x, c in enumerate(f"{int(knothash(f'{content}-{y}'), 16):128b}") if c == "1"}
    regions = 0
    while grid:
        region = {grid.pop()}
        verified: set[tuple[int, int]] = set()
        while verified != region:
            for x, y in region - verified:
                for nb in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
                    if nb in grid:
                        region.add(nb)
                        grid.remove(nb)
                    verified.add((x, y))
        regions += 1
    return regions


test_content = "flqrgnkx"
assert part1(test_content) == 8108
assert part2(test_content) == 1242


content = "nbysizxe"
print(part1(content))
print(part2(content))
