from typing import Any, Iterable

from astar import AStar

content = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

with open("12.txt", "rt") as finput:
    content = finput.read()

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

W, H = x + 1, y + 1


class Day12(AStar):
    def neighbors(self, node) -> Iterable[Any]:
        return (node + x for x in (-1j, 1, 1j, -1) if node + x in grid)

    def distance_between(self, n1, n2) -> float:
        if grid[n2] - 1 == grid[n1]:
            return 0
        elif grid[n2] <= grid[n1]:
            return grid[n1] - grid[n2] + 1
        return float("inf")

    def heuristic_cost_estimate(self, current, goal) -> float:
        c = goal - current
        return abs(c.real) + abs(c.imag) + (grid[goal] - grid[current])


path = list(Day12().astar(start_pos, end_pos))
print(path)
print(len(path) - 1)
print(start_pos, end_pos)

for y in range(H):
    print("".join("*" if complex(x, y) in path else "." for x in range(W)))


s = len(path) - 1
for candidate_start_pos, h in grid.items():
    if h == 0:
        candidate_path = Day12().astar(candidate_start_pos, end_pos)
        if candidate_path is None:
            continue
        candidate_path = list(candidate_path)
        if len(candidate_path) - 1 < s:
            s = len(candidate_path) - 1


print(s)
