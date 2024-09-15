from collections.abc import Iterator
from typing import Any

from astar import AStar  # type: ignore[import-not-found]


class Day12(AStar):  # type: ignore[misc]
    def __init__(self, grid: dict[complex, int]) -> None:
        self.grid = grid

    def neighbors(self, node: complex) -> Iterator[Any]:
        return (node + x for x in (-1j, 1, 1j, -1) if node + x in self.grid)

    def distance_between(self, n1: complex, n2: complex) -> float:
        if self.grid[n2] - 1 == self.grid[n1]:
            return 0
        if self.grid[n2] <= self.grid[n1]:
            return self.grid[n1] - self.grid[n2] + 1
        return float("inf")

    def heuristic_cost_estimate(self, current: complex, goal: complex) -> float:
        c = goal - current
        return abs(c.real) + abs(c.imag) + (self.grid[goal] - self.grid[current])


def solve(content: str) -> Iterator[int]:
    grid: dict[complex, int] = {}
    start_pos: complex
    end_pos: complex
    for y, line in enumerate(content.splitlines()):
        for x, c in enumerate(line):
            p = complex(x, y)
            if c == "S":
                start_pos = p
                h = 0
            elif c == "E":
                end_pos = p
                h = 26
            else:
                h = "abcdefghijklmnopqrstuvwxyz".index(c)
            grid[p] = h

    result = Day12(grid).astar(start_pos, end_pos)
    assert result is not None
    path = list(result)
    yield len(path) - 1
    # W, H = x + 1, y + 1
    # for y in range(H):
    #     print("".join("*" if complex(x, y) in path else "." for x in range(W)))

    s = len(path) - 1
    for candidate_start_pos, h in grid.items():
        if h == 0:
            candidate_path = Day12(grid).astar(candidate_start_pos, end_pos)
            if candidate_path is None:
                continue
            candidate_path = list(candidate_path)
            s = min(len(candidate_path) - 1, s)

    yield s


test_content = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

assert next(solve(test_content)) == 31

with open("12.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
