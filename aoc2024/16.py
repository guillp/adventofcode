from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass
class State:
    cost: int = field(compare=True)
    path: tuple[complex, ...]
    direction: complex

    @property
    def pos(self) -> complex:
        return self.path[-1]

    def next(self) -> Iterator[State]:
        yield State(self.cost + 1, (*self.path, self.pos + self.direction), self.direction)
        yield State(self.cost + 1000, self.path, self.direction * 1j)
        yield State(self.cost + 1000, self.path, self.direction * -1j)


def solve(content: str, *, debug: bool = False) -> tuple[int, int]:
    grid = {
        complex(x, y): c for y, line in enumerate(content.strip().splitlines()) for x, c in enumerate(line) if c != "#"
    }
    start_pos = next(pos for pos, c in grid.items() if c == "S")
    end_pos = next(pos for pos, c in grid.items() if c == "E")

    best_costs = {(start_pos, -1 + 0j): 0}

    pool = deque([State(0, (start_pos,), -1)])
    infinite = len(grid) * 1000
    found_paths: dict[int, list[State]] = {}

    while pool:
        state = pool.popleft()

        if state.cost > best_costs.get((state.pos, state.direction), infinite) or state.cost > min(
            found_paths,
            default=infinite,
        ):
            continue

        for next_state in state.next():
            if next_state.pos not in grid:
                continue
            if next_state.pos == end_pos:
                found_paths.setdefault(next_state.cost, []).append(next_state)
            elif next_state.cost <= best_costs.get((next_state.pos, next_state.direction), infinite):
                best_costs[next_state.pos, next_state.direction] = next_state.cost
                pool.append(next_state)

    best_cost = min(found_paths)
    best_tiles = {tile for state in found_paths[best_cost] for tile in state.path}
    if debug:
        print_grid(grid, best_tiles)
    return best_cost, len(best_tiles)


def print_grid(grid: dict[complex, str], path: set[complex]) -> None:
    min_x = int(min(grid, key=lambda pos: pos.real).real - 1)
    max_x = int(max(grid, key=lambda pos: pos.real).real + 1)
    min_y = int(min(grid, key=lambda pos: pos.imag).imag - 1)
    max_y = int(max(grid, key=lambda pos: pos.imag).imag + 1)
    for y in range(min_y, max_y + 1):
        print("".join(grid.get(p, "#") if (p := x + y * 1j) not in path else "O" for x in range(min_x, max_x + 1)))


test_content = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

test_content2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

assert solve(test_content) == (7036, 45)
assert solve(test_content2) == (11048, 64)

with open("16.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
