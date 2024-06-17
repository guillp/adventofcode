import re
from itertools import count


def scanner_pos(t: int, r: int) -> int:
    match t % ((r - 1) * 2):
        case offset if offset < r - 1:  # scanner going down
            return offset
        case offset if offset >= r - 1:  # scanner going up
            return 2 * (r - 1) - offset
    assert False


def part1(content: str, delay: int = 0) -> int:
    scanners: dict[int, int] = dict(map(int, re.findall(r"\d+", line)) for line in content.strip().splitlines())  # type: ignore[misc]
    severity = 0
    for depth in range(max(scanners) + 1):
        r = scanners.get(depth)
        if r is None:
            continue
        if scanner_pos(delay + depth, r) == 0:
            severity += depth * r
    return severity


def part2(content: str) -> int:
    scanners: dict[int, int] = dict(map(int, re.findall(r"\d+", line)) for line in content.strip().splitlines())  # type: ignore[misc]

    for delay in count():
        for d, r in scanners.items():
            if scanner_pos(d + delay, r) == 0:
                break
        else:
            return delay
    assert False


test_content = """\
0: 3
1: 2
4: 4
6: 4
"""

assert part1(test_content) == 24
assert part2(test_content) == 10

with open("13.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
