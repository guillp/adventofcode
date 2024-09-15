from collections import defaultdict


def manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y2 - y1)


def solve(content: str, dist: int = 10_000) -> tuple[int, int]:
    grid = {tuple(int(x) for x in line.split(", ")) for line in content.splitlines()}
    left = min(x for x, _ in grid)
    right = max(x for x, _ in grid)
    top = min(y for _, y in grid)
    bottom = max(y for _, y in grid)

    areas = defaultdict(set)
    part2 = 0
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            distances = sorted((manhattan(x, y, X, Y), (X, Y)) for X, Y in grid)
            min_dist, (X, Y) = distances[0]
            if distances[1][0] > min_dist:
                areas[X, Y].add((x, y))
            if sum(d for d, _ in distances) < dist:
                part2 += 1

    for area in sorted(areas.values(), key=len, reverse=True):
        if any(x in {left, right} or y in {top, bottom} for x, y in area):
            continue
        part1 = len(area)
        break

    return part1, part2


assert solve(
    """\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""",
    32,
) == (17, 16)

with open("06.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
