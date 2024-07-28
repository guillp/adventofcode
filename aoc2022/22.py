import re
from collections.abc import Callable, Iterator

UP, RIGHT, DOWN, LEFT = -1j, 1, 1j, -1


def solve(content: str) -> Iterator[int]:
    board, instructions = content.rstrip().split("\n\n")

    grid = {}
    for y, line in enumerate(board.splitlines()):
        for x, c in enumerate(line):
            if c in "#.":
                grid[complex(x, y)] = c

    for wrapper in (part1_wrap, part2_wrap):
        pos, heading, path = follow_path(grid, instructions, wrapper)
        yield password(pos, heading)


def part1_wrap(pos: complex, facing: complex, grid: dict[complex, str], face_size: int) -> tuple[complex, complex]:
    next_pos = pos + facing
    while next_pos - facing in grid:
        next_pos -= facing

    return next_pos, facing


def face(pos: complex, face_size: int) -> int:
    """Given a position on the map, return the face number of the cube it belongs to.

    This must be adapted based on your input map shape.
    """
    if 0 <= pos.real < face_size:
        if face_size * 2 <= pos.imag < face_size * 3:
            return 4
        elif face_size * 3 <= pos.imag < face_size * 4:
            return 6
    elif face_size <= pos.real < face_size * 2:
        if 0 <= pos.imag < face_size:
            return 1
        elif face_size <= pos.imag < face_size * 2:
            return 3
        elif face_size * 2 <= pos.imag < face_size * 3:
            return 5
    elif face_size * 2 <= pos.real < face_size * 3 and 0 <= pos.imag < face_size:
        return 2
    assert False, pos


def part2_wrap(pos: complex, heading: complex, grid: dict[complex, str], face_size: int) -> tuple[complex, complex]:
    x = int(pos.real) % face_size
    y = int(pos.imag) % face_size
    current_face = face(pos, face_size)

    next_face, next_heading, next_pos = {  # type: ignore[index]
        1: {
            UP: (6, RIGHT, complex(0, face_size * 3 + x)),
            LEFT: (4, RIGHT, complex(0, face_size * 3 - 1 - y)),
        },
        2: {
            UP: (6, UP, complex(x, face_size * 4 - 1)),
            RIGHT: (5, LEFT, complex(face_size * 2 - 1, face_size * 3 - 1 - y)),
            DOWN: (3, LEFT, complex(face_size * 2 - 1, face_size + x)),
        },
        3: {
            LEFT: (4, DOWN, complex(y, face_size * 2)),
            RIGHT: (2, UP, complex(face_size * 2 + y, face_size - 1)),
        },
        4: {
            UP: (3, RIGHT, complex(face_size, face_size + x)),
            LEFT: (1, RIGHT, complex(face_size, face_size - 1 - y)),
        },
        5: {
            RIGHT: (2, LEFT, complex(face_size * 3 - 1, face_size - 1 - y)),
            DOWN: (6, LEFT, complex(face_size - 1, face_size * 3 + x)),
        },
        6: {
            RIGHT: (5, UP, complex(face_size + y, face_size * 3 - 1)),
            DOWN: (2, DOWN, complex(face_size * 2 + x, 0)),
            LEFT: (1, DOWN, complex(face_size + y, 0)),
        },
    }[current_face][heading]

    assert next_face == face(
        next_pos, face_size
    ), f"{current_face} -> {next_face}, {pos} -> {next_pos}, {heading} -> {next_heading}, {x=}, {y=}"
    assert (
        next_pos in grid
    ), f"{current_face} -> {next_face}, {pos} -> {next_pos}, {heading} -> {next_heading}, {x=}, {y=}"
    return next_pos, next_heading


def follow_path(
    grid: dict[complex, str],
    instructions: str,
    wrap_method: Callable[[complex, complex, dict[complex, str], int], tuple[complex, complex]],
) -> tuple[complex, complex, dict[complex, str]]:
    W = int(max(pos.real for pos in grid))
    face_size = W // 3 + 1
    path = grid.copy()
    pos = complex(next(x for x in range(W) if grid.get(complex(x, 0)) == "."), 0)

    heading = UP
    for turn, steps in re.findall(r"([RL])(\d+)", "R" + instructions):
        if turn == "R":
            heading *= 1j
        else:
            heading *= -1j

        for _ in range(int(steps)):
            next_pos = pos + heading
            # turn around the cube
            if next_pos not in grid:
                next_pos, next_heading = wrap_method(pos, heading, grid, face_size)
                assert wrap_method(next_pos, -next_heading, grid, face_size) == (pos, -heading)
            else:
                next_heading = heading

            next_tile = grid[next_pos]
            if next_tile == ".":
                pos = next_pos
                heading = next_heading
            elif next_tile == "#":
                break

        path[pos] = {RIGHT: ">", DOWN: "v", LEFT: "<", UP: "^"}[heading]
    return pos, heading, path


def password(pos: complex, heading: complex) -> int:
    return int(pos.imag + 1) * 1000 + int(pos.real + 1) * 4 + {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}[heading]


test_content = """\
        ...#
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

assert tuple(solve(test_content)) == (6032, 5031)  # This doesn't work due to map shape being different that input

with open("22.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
