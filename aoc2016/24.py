from collections.abc import Callable, Iterator
from itertools import count
from operator import itemgetter


def flood_fill(
    grid: dict[complex, str],
    start: complex,
    is_interesting: Callable[[str], bool],
) -> Iterator[tuple[str, int]]:
    seen: set[complex] = set()
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


def grid_to_graph(grid: dict[complex, str], paths: str = ".") -> dict[str, dict[str, int]]:
    G = {}
    points = {pos: cell for pos, cell in grid.items() if cell not in paths}
    for pos, cell in points.items():
        G[cell] = dict(flood_fill(grid, pos, is_interesting=lambda c: c.isdigit()))
    return G


def solve(
    content: str,
    part2: bool = False,
) -> int:
    grid = {complex(x, y): c for y, line in enumerate(content.splitlines()) for x, c in enumerate(line) if c != "#"}
    G = grid_to_graph(grid)
    targets = frozenset(G)
    pool: list[tuple[int, tuple[str, ...]]] = [(0, ("0",))]
    best = None
    while pool:
        pool.sort(key=itemgetter(0))
        cost, visited = pool.pop()
        if best is not None and cost >= best:
            continue
        remaining = targets - set(visited)
        if not remaining:
            if part2:
                cost += G[visited[-1]][visited[0]]
            if best is None or cost < best:
                best = cost
        else:
            for next_target in targets.difference(visited):
                next_cost = G[visited[-1]][next_target]
                pool.append((cost + next_cost, visited + (next_target,)))

    if best is None:
        raise ValueError("Solution not found!")
    return best


test_content = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""

assert solve(test_content) == 14


with open("24.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
