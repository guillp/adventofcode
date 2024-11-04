from collections.abc import Iterator
from heapq import heappop, heappush
from itertools import product


def solve(content: str, *, part2: bool = False) -> int:
    lines = content.strip().splitlines()
    grid = {(x, y): int(c) for y, line in enumerate(lines) for x, c in enumerate(line)}
    height, width = len(lines), len(lines[0])
    assert height == width
    if part2:
        base_grid = grid
        grid = {}
        for i, j in product(range(5), repeat=2):
            for (x, y), r in base_grid.items():
                grid[x + i * width, y + j * height] = (r + i + j - 1) % 9 + 1
        height *= 5
        width *= 5

    # get the risk score for a direct diagonal as an upper bound solution
    diagonal_solution = sum(grid[x, x] for x in range(width)) + sum(grid[x + 1, x] for x in range(width - 1))

    # A* algorithm
    predecessors = dict[tuple[int, int], tuple[int, int]]()

    def reconstruct(x: int, y: int) -> Iterator[tuple[int, int]]:
        yield x, y
        while (x, y) in predecessors:
            x, y = predecessors[x, y]
            yield x, y

    def heuristic(x: int, y: int) -> int:
        return width - 1 - x + height - 1 - y

    opened = [(diagonal_solution, (0, 0))]
    g_scores = {(0, 0): 0}

    while opened:
        _, (x, y) = heappop(opened)
        if (x, y) == (width - 1, height - 1):
            path = list(reconstruct(x, y))
            return sum(grid[pos] for pos in path[:-1])

        for next_x, next_y in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
            if (next_x, next_y) not in grid:
                continue
            g_score = g_scores[x, y] + grid[next_x, next_y]
            if g_score < g_scores.get((next_x, next_y), diagonal_solution):
                predecessors[next_x, next_y] = x, y
                g_scores[next_x, next_y] = g_score
                heappush(opened, (g_score + heuristic(next_x, next_y), (next_x, next_y)))

    assert False, "Solution not found!"


test_content = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
assert solve(test_content) == 40
assert solve(test_content, part2=True) == 315

with open("15.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
