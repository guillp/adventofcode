from itertools import count

type Grid = dict[tuple[int, int], str]


def roll(grid: Grid, height: int, width: int) -> Grid:
    target = grid.copy()
    for x in range(width):
        stop = 0
        for y in range(height):
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


def get_load(grid: Grid, height: int, width: int) -> int:
    return sum(height - y for x in range(width) for y in range(height) if grid[x, y] == "O")


def rotate(grid: Grid, height: int) -> Grid:
    return {(height - y - 1, x): c for (x, y), c in grid.items()}


def part2(content: str) -> int:
    lines = content.splitlines()
    height = len(lines)
    width = len(lines[0])
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    states = [grid]
    for i in count(1):
        for _ in range(4):
            grid = roll(grid, height, width)
            grid = rotate(grid, height)
            height, width = width, height

        try:
            j = states.index(grid)  # loop found
        except ValueError:
            states.append(grid)
        else:
            k = (1000000000 - j) % (i - j) + j
            return get_load(states[k], height, width)

    assert False, "Solution not found!"


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

assert part1(test_content) == 136
assert part2(test_content) == 64

with open("14.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
