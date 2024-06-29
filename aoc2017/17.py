from collections import deque


def part1(steps: int) -> int:
    buffer = deque([0])
    for i in range(2017):
        buffer.rotate(-steps)
        buffer.append(i + 1)
    return buffer[0]


def part2(steps: int) -> int:
    buffer = deque([0])
    for i in range(50_000_000):
        buffer.rotate(-steps)
        buffer.append(i + 1)
    return buffer[buffer.index(0) + 1]


assert part1(3) == 638
print(part1(344))
print(part2(344))
