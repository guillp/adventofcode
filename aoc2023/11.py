from collections.abc import Iterator
from itertools import combinations


def expand(galaxies: tuple[tuple[int, int], ...], height: int, width: int, d: int) -> tuple[tuple[int, int], ...]:
    x_shift = y_shift = 0
    for x in range(width):
        if not any(galaxy[0] == x + x_shift for galaxy in galaxies):
            galaxies = tuple((gx + d, gy) if gx >= x + x_shift else (gx, gy) for (gx, gy) in galaxies)
            x_shift += d
    for y in range(height):
        if not any(galaxy[1] == y + y_shift for galaxy in galaxies):
            galaxies = tuple((gx, gy + d) if gy >= y + y_shift else (gx, gy) for (gx, gy) in galaxies)
            y_shift += d

    return galaxies


def solve(content: str, magnification: int = 1_000_000) -> Iterator[int]:
    lines = content.splitlines()
    H = len(lines)
    W = len(lines[0])
    galaxies = tuple((x, y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == "#")

    galaxies1 = expand(galaxies, H, W, 1)

    part1 = 0
    for (x1, y1), (x2, y2) in combinations(galaxies1, 2):
        dist = abs(x2 - x1) + abs(y2 - y1)
        part1 += dist
    yield part1

    galaxies2 = expand(galaxies, H, W, magnification - 1)
    part2 = 0
    for (x1, y1), (x2, y2) in combinations(galaxies2, 2):
        dist = abs(x2 - x1) + abs(y2 - y1)
        part2 += dist
    yield part2


test_content = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

assert tuple(solve(test_content, magnification=10)) == (374, 1030)
assert tuple(solve(test_content, magnification=100)) == (374, 8410)

with open("11.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
