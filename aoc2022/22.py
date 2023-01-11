import re
import sys
from typing import Callable

content = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

with open("22.txt") as f:    content = f.read()


def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)


board, instructions = content.rstrip().split("\n\n")

grid = {}
for y, line in enumerate(board.splitlines()):
    for x, c in enumerate(line):
        if c in "#.":
            grid[complex(x, y)] = c

W = int(max(pos.real for pos in grid))
H = int(max(pos.imag for pos in grid))
FACE_SIZE = W // 3 + 1
UP, RIGHT, DOWN, LEFT = -1j, 1, 1j, -1


def part1_wrap(
        pos: complex, facing: complex, grid: dict[complex, str]
) -> tuple[complex, complex]:
    next_pos = pos + facing
    while next_pos - facing in grid:
        next_pos -= facing

    return next_pos, facing, face(pos)


def face(pos: complex) -> int:
    if 0 <= pos.real < FACE_SIZE:
        if FACE_SIZE * 2 <= pos.imag < FACE_SIZE * 3:
            return 4
        elif FACE_SIZE * 3 <= pos.imag < FACE_SIZE * 4:
            return 6
    elif FACE_SIZE <= pos.real < FACE_SIZE * 2:
        if 0 <= pos.imag < FACE_SIZE:
            return 1
        elif FACE_SIZE <= pos.imag < FACE_SIZE * 2:
            return 3
        elif FACE_SIZE * 2 <= pos.imag < FACE_SIZE * 3:
            return 5
    elif FACE_SIZE * 2 <= pos.real < FACE_SIZE * 3:
        if 0 <= pos.imag < FACE_SIZE:
            return 2
    assert False, pos


def part2_wrap(
        pos: complex, heading: complex, grid: dict[complex, str]
) -> tuple[complex, complex]:
    x = int(pos.real) % FACE_SIZE
    y = int(pos.imag) % FACE_SIZE
    current_face = face(pos)

    next_face, next_heading, next_pos = {
        1: {
            UP: (6, RIGHT, complex(0, FACE_SIZE * 3 + x)),
            LEFT: (4, RIGHT, complex(0, FACE_SIZE * 3 - 1 - y)),
        },
        2: {
            UP: (6, UP, complex(x, FACE_SIZE * 4 - 1)),
            RIGHT: (5, LEFT, complex(FACE_SIZE * 2 - 1, FACE_SIZE * 3 - 1 - y)),
            DOWN: (3, LEFT, complex(FACE_SIZE * 2 - 1, FACE_SIZE + x)),
        },
        3: {
            LEFT: (4, DOWN, complex(y, FACE_SIZE * 2)),
            RIGHT: (2, UP, complex(FACE_SIZE * 2 + y, FACE_SIZE - 1)),
        },
        4: {
            UP: (3, RIGHT, complex(FACE_SIZE, FACE_SIZE + x)),
            LEFT: (1, RIGHT, complex(FACE_SIZE, FACE_SIZE - 1 - y))
        },
        5: {
            RIGHT: (2, LEFT, complex(FACE_SIZE * 3 - 1, FACE_SIZE - 1 - y)),
            DOWN: (6, LEFT, complex(FACE_SIZE - 1, FACE_SIZE * 3 + x))
        },
        6: {
            RIGHT: (5, UP, complex(FACE_SIZE + y, FACE_SIZE * 3 - 1)),
            DOWN: (2, DOWN, complex(FACE_SIZE * 2 + x, 0)),
            LEFT: (1, DOWN, complex(FACE_SIZE + y, 0)),
        }
    }[current_face][heading]

    debug(f"{current_face} -> {next_face}, {pos} -> {next_pos}, {heading} -> {next_heading}, {x=}, {y=}")
    assert next_face == face(
        next_pos), f"{current_face} -> {next_face}, {pos} -> {next_pos}, {heading} -> {next_heading}, {x=}, {y=}"
    assert next_pos in grid, f"{current_face} -> {next_face}, {pos} -> {next_pos}, {heading} -> {next_heading}, {x=}, {y=}"
    return next_pos, next_heading


def follow_path(
        grid: dict[complex, str],
        instructions: str,
        wrap_method: Callable[
            [complex, complex, dict[complex, str]], tuple[complex, complex]
        ],
):
    path = grid.copy()
    pos = complex(next(x for x in range(W) if grid.get(complex(x, 0)) == "."), 0)
    debug("initial pos:", pos)
    heading = UP
    for turn, steps in re.findall("([RL])(\d+)", "R" + instructions):
        debug(turn, steps)
        if turn == "R":
            heading *= 1j
        else:
            heading *= -1j

        for i in range(int(steps)):
            next_pos = pos + heading
            # turn around the cube
            if next_pos not in grid:
                next_pos, next_heading = wrap_method(pos, heading, grid)
                assert wrap_method(next_pos, -next_heading, grid) == (pos, -heading)
            else:
                next_heading = heading

            next_tile = grid[next_pos]
            if next_tile == ".":
                pos = next_pos
                heading = next_heading
            elif next_tile == "#":
                break
        debug(pos+1+1j, {1: "R", 1j: "D", -1: "L", -1j: "U"}[heading])
        path[pos] = {1: ">", 1j: "v", -1: "<", -1j: "^"}[heading]
    return pos, heading, path


def password(pos: complex, heading: complex) -> int:
    return (
            int(pos.imag + 1) * 1000 + int(pos.real + 1) * 4 + {1: 0, 1j: 1, -1: 2, -1j: 3}[heading]
    )


# print(password(*follow_path(grid, instructions, part1_wrap)), flush=True)
pos, heading, path = follow_path(grid, instructions, part2_wrap)
for y in range(H):
    print("".join(path.get(complex(x,y), " ") for x in range(W)))

print(password(pos, heading))
