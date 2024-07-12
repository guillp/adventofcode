from enum import Enum

Point = tuple[int, int]


class Direction(Enum):
    NORTH = 0, -1
    SOUTH = 0, 1
    EAST = 1, 0
    WEST = -1, 0


def continue_path(grid: dict[Point, str], cell: Point, direction: Direction) -> int:
    paths = {(cell, direction)}
    pool = {(cell, direction)}
    while pool:
        cell, direction = pool.pop()
        x, y = cell
        match direction:
            case Direction.NORTH:
                next_cell = (x, y - 1)
            case Direction.SOUTH:
                next_cell = (x, y + 1)
            case Direction.EAST:
                next_cell = (x + 1, y)
            case Direction.WEST:
                next_cell = (x - 1, y)
            case _:
                assert False

        if (next_cell, direction) in paths:
            continue  # avoid loops

        match grid.get(next_cell):
            case None:  # out of grid
                continue
            case "|":  # splitter
                match direction:
                    case Direction.EAST | Direction.WEST:
                        pool |= {
                            (next_cell, Direction.NORTH),
                            (next_cell, Direction.SOUTH),
                        }
                    case Direction.NORTH | Direction.SOUTH:
                        pool |= {(next_cell, direction)}
            case "-":  # splitter
                match direction:
                    case Direction.NORTH | Direction.SOUTH:
                        pool |= {
                            (next_cell, Direction.EAST),
                            (next_cell, Direction.WEST),
                        }
                    case Direction.EAST | Direction.WEST:
                        pool |= {(next_cell, direction)}
            case "\\":  # mirror
                match direction:
                    case Direction.NORTH:
                        pool |= {(next_cell, Direction.WEST)}
                    case Direction.SOUTH:
                        pool |= {(next_cell, Direction.EAST)}
                    case Direction.EAST:
                        pool |= {(next_cell, Direction.SOUTH)}
                    case Direction.WEST:
                        pool |= {(next_cell, Direction.NORTH)}
            case "/":  # mirror
                match direction:
                    case Direction.NORTH:
                        pool |= {(next_cell, Direction.EAST)}
                    case Direction.SOUTH:
                        pool |= {(next_cell, Direction.WEST)}
                    case Direction.EAST:
                        pool |= {(next_cell, Direction.NORTH)}
                    case Direction.WEST:
                        pool |= {(next_cell, Direction.SOUTH)}
            case ".":
                pool |= {(next_cell, direction)}
            case _:
                assert False

        paths.add((next_cell, direction))

    return len({cell for cell, direction in paths})


def part1(content: str) -> int:
    grid = {(x, y): c for y, line in enumerate(content.strip().splitlines()) for x, c in enumerate(line)}
    return continue_path(grid, (0, 0), Direction.EAST)


def part2(content: str) -> int:
    lines = content.strip().splitlines()
    H = len(lines)
    W = len(lines[0])
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    return max(
        *(continue_path(grid, (x, 0), Direction.SOUTH) for x in range(W)),
        *(continue_path(grid, (x, H), Direction.NORTH) for x in range(W)),
        *(continue_path(grid, (0, y), Direction.EAST) for y in range(H)),
        *(continue_path(grid, (W, y), Direction.WEST) for y in range(H)),
    )


test_content = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


assert part1(test_content) == 46
assert part2(test_content) == 51

with open("16.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
