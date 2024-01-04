# traveling-salesman
from collections import defaultdict
from heapq import heappop, heappush, heapify
from itertools import count
from operator import itemgetter
from typing import Callable, Any, Iterator

test_content = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""


def flood_fill(
    grid: dict[complex, dict[complex, int]],
    start: complex,
    is_interesting: Callable[[str], bool],
) -> Iterator[tuple[complex, int]]:
    seen = set()
    phase = {start}
    walkables = frozenset(grid)
    for i in count(1):
        next_phase = set()
        for cell in phase:
            for next_cell in {
                cell + 1,
                cell - 1,
                cell + 1j,
                cell - 1j,
            } & walkables - seen:
                if is_interesting(grid[next_cell]):
                    yield grid[next_cell], i
                next_phase.add(next_cell)
                seen.add(next_cell)
        if next_phase:
            phase = next_phase
        else:
            break


def parse_grid(content: str, walls="#") -> tuple[dict[complex, str], int, int]:
    lines = content.splitlines()
    H = len(lines)
    W = len(lines[0])

    grid = {
        complex(x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c not in walls
    }

    return grid, W, H


def grid_to_graph(
    grid: dict[complex, str], paths: str = "."
) -> dict[complex, dict[complex, int]]:
    G = {}
    points = {pos: cell for pos, cell in grid.items() if cell not in paths}
    for pos, cell in points.items():
        G[cell] = dict(flood_fill(grid, pos, is_interesting=lambda c: c.isdigit()))
    return G


def traveling_salesman(
    G: dict[complex, dict[complex, int]], *start_positions: complex, back_to_origin: bool=False
) -> int:
    targets = frozenset(G)
    pool = [(0, (pos,)) for pos in start_positions]
    best = float('inf')
    while pool:
        pool.sort(key=itemgetter(0))
        cost, visited = pool.pop()
        if cost >= best:
            continue
        remaining = targets-set(visited)
        if not remaining:
            if back_to_origin:
                cost += G[visited[-1]][visited[0]]
            best = min(best, cost)
        else:
            for next_target in targets.difference(visited):
                next_cost = G[visited[-1]][next_target]
                pool.append((cost+next_cost, visited + (next_target,)))

    return best


with open("24.txt") as f:
    content = f.read()
grid, W, H = parse_grid(content)
G = grid_to_graph(grid)
print(traveling_salesman(G, "0"))
print(traveling_salesman(G, "0", back_to_origin=True))