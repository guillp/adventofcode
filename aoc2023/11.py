import math
from itertools import combinations
from typing import Iterable

content = """\
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

with open('11.txt') as f: content = f.read()

lines = content.splitlines()
H = len(lines)
W = len(lines[0])
galaxies = tuple((x, y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == "#")


def expand(galaxies: tuple[tuple[int, int]], H: int, W: int, d: int):
    x_shift = y_shift = 0
    for x in range(W):
        if not any(galaxy[0] == x + x_shift for galaxy in galaxies):
            galaxies = tuple((gx + d, gy) if gx >= x + x_shift else (gx, gy) for (gx, gy) in galaxies)
            x_shift += d
    for y in range(H):
        if not any(galaxy[1] == y + y_shift for galaxy in galaxies):
            galaxies = tuple((gx, gy + d) if gy >= y + y_shift else (gx, gy) for (gx, gy) in galaxies)
            y_shift += d

    return galaxies


galaxies1 = expand(galaxies, H, W, 1)

s = 0
for (x1, y1), (x2, y2) in combinations(galaxies1, 2):
    dist = abs(x2 - x1) + abs(y2 - y1)
    s += dist

print(s)

galaxies2 = expand(galaxies, H, W, 999_999)
s2 = 0
for (x1, y1), (x2, y2) in combinations(galaxies2, 2):
    dist = abs(x2 - x1) + abs(y2 - y1)
    s2 += dist

print(s2)
