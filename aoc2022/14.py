from collections.abc import Iterator
from itertools import pairwise


def print_grid(grid: dict[complex, str]) -> None:
    top = 0
    bottom = int(max(pos.imag for pos in grid))
    left = int(min(pos.real for pos in grid)) - 2
    right = int(max(pos.real for pos in grid)) + 2
    for y in range(top, bottom + 1):
        print(
            f"{y:02d}",
            "".join(grid.get(complex(x, y), ".") for x in range(left, right + 1)),
        )


def solve(content: str) -> Iterator[int]:
    grid = {}
    for line in content.splitlines():
        coords = [(int(x), int(y)) for coord in line.split(" -> ") for x, y in [coord.split(",")]]
        for (x1, y1), (x2, y2) in pairwise(coords):
            if x1 == x2:
                if y2 < y1:
                    y1, y2 = y2, y1
                for y in range(y1, y2 + 1):
                    grid[complex(x1, y)] = "#"
            elif y1 == y2:
                if x2 < x1:
                    x1, x2 = x2, x1
                for x in range(x1, x2 + 1):
                    grid[complex(x, y1)] = "#"
            else:
                assert False

    bottom = int(max(pos.imag for pos in grid))

    def next_sand() -> bool:
        sand = 500 + 0j
        while sand.imag < bottom:
            if sand + 1j not in grid:
                sand += 1j
            elif sand - 1 + 1j not in grid:
                sand += -1 + 1j
            elif sand + 1 + 1j not in grid:
                sand += 1 + 1j
            elif sand in grid:
                return False
            else:
                grid[sand] = "o"
                return True
        return False

    i = 0
    while next_sand():
        i += 1

    # print_grid()
    yield i

    bottom += 2

    class BottomGrid(dict[complex, str]):
        def __getitem__(self, item: complex) -> str:
            if isinstance(item, complex) and item.imag == bottom:
                return "#"
            return super().__getitem__(item)

        def __contains__(self, item: object) -> bool:
            if isinstance(item, complex) and item.imag == bottom:
                return True
            return super().__contains__(item)

    grid = BottomGrid(grid)

    while next_sand():
        i += 1

    # print_grid()
    yield i


test_content = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

assert tuple(solve(test_content)) == (24, 93)

with open("14.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
