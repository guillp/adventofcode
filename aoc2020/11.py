from collections.abc import Callable, Iterator
from enum import Enum
from itertools import product


class Seat(str, Enum):
    OCCUPIED = "#"
    EMPTY = "L"
    FLOOR = "."


def solve(content: str) -> Iterator[int]:
    lines = content.strip().splitlines()

    grid = {(x, y): Seat(c) for y, line in enumerate(lines) for x, c in enumerate(line)}

    def occupied_neighbors_part1(grid: dict[tuple[int, int], Seat], x: int, y: int) -> Iterator[tuple[int, int]]:
        for xn in (x - 1, x, x + 1):
            for yn in (y - 1, y, y + 1):
                if not (xn == x and yn == y) and grid.get((xn, yn)) == Seat.OCCUPIED:
                    yield xn, yn

    def occupied_neighbors_part2(grid: dict[tuple[int, int], Seat], x: int, y: int) -> Iterator[tuple[int, int]]:
        for xd, yd in product((-1, 0, 1), repeat=2):
            if xd == yd == 0:
                continue
            dist = 1
            while True:
                match grid.get((x + dist * xd, y + dist * yd)):
                    case Seat.FLOOR:
                        dist += 1
                    case Seat.EMPTY | None:
                        break
                    case Seat.OCCUPIED:
                        yield x + dist * xd, y + dist * yd
                        break

    def simulate(
        grid: dict[tuple[int, int], Seat],
        occupied_func: Callable[[dict[tuple[int, int], Seat], int, int], Iterator[tuple[int, int]]],
        occupied_tolerance: int,
    ) -> int:
        states = [grid]
        while len(states) == 1 or states[-1] != states[-2]:
            new_grid = dict[tuple[int, int], Seat]()
            for (x, y), c in states[-1].items():
                occupied_neighbors = tuple(occupied_func(states[-1], x, y))
                match c, len(occupied_neighbors):
                    case Seat.EMPTY, 0:
                        new_grid[x, y] = Seat.OCCUPIED
                    case Seat.OCCUPIED, nb if nb >= occupied_tolerance:
                        new_grid[x, y] = Seat.EMPTY
                    case _:
                        new_grid[x, y] = c
            states.append(new_grid)

        return sum(c == Seat.OCCUPIED for c in states[-1].values())

    yield simulate(grid, occupied_neighbors_part1, 4)
    yield simulate(grid, occupied_neighbors_part2, 5)


assert tuple(
    solve("""\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""),
) == (37, 26)

with open("11.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
