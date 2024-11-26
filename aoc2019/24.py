from collections import defaultdict
from collections.abc import Iterable
from itertools import product


def print_grid(grid: set[tuple[int, int]]) -> None:
    for y in range(5):
        print("".join("#" if (x, y) in grid else "." for x in range(5)))
    print()


def part1(content: str) -> int:
    grid = frozenset(
        (x, y) for y, line in enumerate(content.strip().splitlines()) for x, c in enumerate(line) if c == "#"
    )

    def step(grid: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
        return frozenset(
            (x, y)
            for y in range(5)
            for x in range(5)
            if (
                (nb := sum((xn, yn) in grid for xn, yn in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)))) == 1
                and (x, y) in grid
            )
            or (nb in (1, 2) and (x, y) not in grid)
        )

    history = set()
    while True:
        if grid in history:
            return sum(2 ** (y * 5 + x) for y in range(5) for x in range(5) if (x, y) in grid)
        history.add(grid)
        # print_grid(grid)
        grid = step(grid)


def recursive_neighbors(x: int, y: int, z: int) -> Iterable[tuple[int, int, int]]:
    if x == y == 2:
        return

    if x == 0:
        yield 1, 2, z - 1
    if x == 1 and y == 2:
        for yn in range(5):
            yield 0, yn, z + 1
    elif x < 4:
        yield x + 1, y, z
    if x == 3 and y == 2:
        for yn in range(5):
            yield 4, yn, z + 1
    elif x > 0:
        yield x - 1, y, z
    if x == 4:
        yield 3, 2, z - 1

    if y == 0:
        yield 2, 1, z - 1
    if y == 1 and x == 2:
        for xn in range(5):
            yield xn, 0, z + 1
    elif y < 4:
        yield x, y + 1, z
    if y == 3 and x == 2:
        for xn in range(5):
            yield xn, 4, z + 1
    elif y > 0:
        yield x, y - 1, z
    if y == 4:
        yield 2, 3, z - 1


assert set(recursive_neighbors(3, 3, 0)) == {(3, 2, 0), (2, 3, 0), (4, 3, 0), (3, 4, 0)}
assert set(recursive_neighbors(1, 1, 0)) == {(1, 0, 0), (0, 1, 0), (2, 1, 0), (1, 2, 0)}
assert set(recursive_neighbors(3, 0, 0)) == {(2, 1, -1), (2, 0, 0), (4, 0, 0), (3, 1, 0)}
assert set(recursive_neighbors(4, 0, 1)) == {(2, 1, 0), (3, 0, 1), (3, 2, 0), (4, 1, 1)}
assert set(recursive_neighbors(3, 2, 1)) == {  # 14
    (3, 1, 1),  # 9
    (4, 0, 2),  # E
    (4, 1, 2),  # J
    (4, 2, 2),  # O
    (4, 3, 2),  # T
    (4, 4, 2),  # Y
    (4, 2, 1),  # 15
    (3, 3, 1),  # 19
}
assert set(recursive_neighbors(3, 2, 0)) == {  # N
    (3, 1, 0),  # I
    (4, 2, 0),  # O
    (3, 3, 0),  # S
    (4, 0, 1),  # five
    (4, 1, 1),
    (4, 2, 1),  # more
    (4, 3, 1),
    (4, 4, 1),  # tiles
}
assert set(recursive_neighbors(0, 4, 1)) == {  # U
    (0, 3, 1),  # P
    (1, 4, 1),  # V
    (2, 3, 0),  # 18
    (1, 2, 0),  # 12
}


def part2(content: str, minutes: int = 200) -> int:
    grid: dict[int, set[tuple[int, int]]] = defaultdict(
        set,
        {0: {(x, y) for y, line in enumerate(content.strip().splitlines()) for x, c in enumerate(line) if c == "#"}},
    )

    def step(grid: dict[int, set[tuple[int, int]]]) -> dict[int, set[tuple[int, int]]]:
        new_grid: dict[int, set[tuple[int, int]]] = defaultdict(set)
        for z in range(min(grid) - 1, max(grid) + 2):
            bugs = grid[z]
            for x, y in product(range(5), repeat=2):
                nb = sum((xn, yn) in grid[zn] for xn, yn, zn in recursive_neighbors(x, y, z))

                if ((x, y) in bugs and nb == 1) or ((x, y) not in bugs and nb in (1, 2)):
                    new_grid[z].add((x, y))

        return new_grid

    for _ in range(minutes):
        grid = step(grid)

    # for layer in sorted(grid):
    #    print(layer, len(grid[layer]))
    #    print_grid(grid[layer])

    return sum(len(layer) for layer in grid.values())


test_content = """\
....#
#..#.
#..##
..#..
#...."""
assert part1(test_content) == 2129920
assert part2(test_content, 10) == 99

with open("24.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
