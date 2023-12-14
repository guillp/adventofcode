from itertools import count
from typing import TypeAlias

test_content = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

with open("14.txt") as f:
    content = f.read()

Grid: TypeAlias = dict[tuple[int, int], str]


def roll(grid: Grid, H: int, W: int) -> Grid:
    target = dict(grid)
    for x in range(W):
        stop = 0
        for y in range(H):
            match grid[x, y]:
                case "#":
                    stop = y + 1
                case "O":
                    if y > stop:
                        target[x, y] = "."
                        target[x, stop] = "O"
                    stop += 1
    return target


def part1(content: str) -> int:
    lines = content.splitlines()
    H = len(lines)
    W = len(lines[0])
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}

    grid = roll(grid, H, W)

    return get_load(grid, H, W)


def get_load(grid: Grid, H: int, W: int) -> int:
    load = 0
    for x in range(W):
        for y in range(H):
            if grid[x, y] == "O":
                load += H - y
    return load


assert part1(test_content) == 136
print(part1(content))


def rotate(grid: Grid, H: int) -> Grid:
    return {(H - y - 1, x): c for (x, y), c in grid.items()}


def part2(content: str) -> int:
    lines = content.splitlines()
    H = len(lines)
    W = len(lines[0])
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    states = [grid]
    for i in count(1):
        grid = roll(grid, H, W)  # north
        grid = rotate(grid, H)
        grid = roll(grid, W, H)  # west
        grid = rotate(grid, W)
        grid = roll(grid, H, W)  # south
        grid = rotate(grid, H)
        grid = roll(grid, W, H)  # east
        grid = rotate(grid, W)

        try:
            j = states.index(grid)  # loop found
            k = (1000000000 - j) % (i - j) + j
            return get_load(states[k], H, W)
        except ValueError:
            states.append(grid)


assert part2(test_content) == 64
print(part2(content))
