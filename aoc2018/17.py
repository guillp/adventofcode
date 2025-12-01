import re
from collections import defaultdict
from collections.abc import Iterator
from enum import Enum


class Cell(str, Enum):
    CLAY = "#"
    SPRING = "+"
    SAND = " "
    FLOW = "|"
    STILL = "~"

    def __repr__(self) -> str:
        return self.value


def solve(content: str) -> Iterator[int]:
    def iter_clays() -> Iterator[tuple[int, int]]:
        for line in content.strip().splitlines():
            a, b, c = (int(n) for n in re.findall(r"\d+", line))
            if line.startswith("x"):
                for y in range(b, c + 1):
                    yield a, y
            elif line.startswith("y"):
                for x in range(b, c + 1):
                    yield x, a

    grid = defaultdict(lambda: Cell.SAND, dict.fromkeys(iter_clays(), Cell.CLAY))

    x_min = min(x for x, y in grid) - 1
    x_max = max(x for x, y in grid) + 1
    y_min = min(y for x, y in grid)
    y_max = max(y for x, y in grid)

    grid[500, 0] = Cell.SPRING

    def print_grid() -> None:
        print("     ", *(x // 100 for x in range(x_min, x_max + 1)), sep="")
        print("     ", *(x // 10 % 10 for x in range(x_min, x_max + 1)), sep="")
        print("     ", *(x % 10 for x in range(x_min, x_max + 1)), sep="")
        for y in range(y_min, y_max + 2):
            print(f"{y: >4}", "".join(grid[x, y] for x in range(x_min, x_max + 1)))
        print()

    def flow_down(x: int, y: int) -> None:
        while y < y_max and grid[x, y + 1] == Cell.SAND:
            grid[x, y + 1] = Cell.FLOW
            y += 1
        if y == y_max:
            return
        flow_side(x, y)

    def flow_side(x: int, y: int) -> None:
        while True:
            grid[x, y] = Cell.FLOW
            left = right = x
            while grid[left - 1, y] in (Cell.SAND, Cell.FLOW) and grid[left, y + 1] in (Cell.CLAY, Cell.STILL):
                left -= 1
                grid[left, y] = Cell.FLOW
            while grid[right + 1, y] in (Cell.SAND, Cell.FLOW) and grid[right, y + 1] in (Cell.CLAY, Cell.STILL):
                right += 1
                grid[right, y] = Cell.FLOW
            if grid[left - 1, y] == grid[right + 1, y] == Cell.CLAY:
                for c in range(left, right + 1):
                    grid[c, y] = Cell.STILL
                y -= 1
            else:
                if grid[left, y + 1] == Cell.SAND:
                    flow_down(left, y)
                if grid[right, y + 1] == Cell.SAND:
                    flow_down(right, y)
                break

    flow_down(500, 0)
    # print_grid()

    still = sum(cell == Cell.STILL for cell in grid.values())
    flowing = sum(cell == Cell.FLOW for (x, y), cell in grid.items() if y >= y_min)
    yield still + flowing
    yield still


test_content = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""

assert tuple(solve(test_content)) == (57, 29)

with open("17.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
