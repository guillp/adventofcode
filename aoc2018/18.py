from collections.abc import Iterable, Iterator
from types import SimpleNamespace


class Acre(SimpleNamespace):
    OPEN = "."
    TREES = "|"
    LUMBERYARD = "#"


def neighbors(p: complex) -> Iterable[complex]:
    for y in (-1, 0, 1):
        for x in (-1, 0, 1):
            if not x == y == 0:
                yield complex(p.real + x, p.imag + y)


def part1(content: str, minutes: int = 10) -> int:
    lines = content.strip().splitlines()
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}

    def step(grid: dict[complex, str]) -> Iterator[tuple[complex, str]]:
        for pos, acre in grid.items():
            match acre:
                case Acre.OPEN if sum(grid.get(nb) == Acre.TREES for nb in neighbors(pos)) >= 3:
                    yield pos, Acre.TREES
                case Acre.TREES if sum(grid.get(nb) == Acre.LUMBERYARD for nb in neighbors(pos)) >= 3:
                    yield pos, Acre.LUMBERYARD
                case Acre.LUMBERYARD if not any(grid.get(nb) == Acre.LUMBERYARD for nb in neighbors(pos)) or not any(
                    grid.get(nb) == Acre.TREES for nb in neighbors(pos)
                ):
                    yield pos, Acre.OPEN
                case _:
                    yield pos, acre

    history = []
    for minute in range(1, minutes + 1):
        history.append(grid)
        grid = dict(step(grid))
        try:
            previous = history.index(grid)
            div, mod = divmod(minutes - minute, minute - previous)
            # print(f"Loop at {previous} -> {minute}, size {minute-previous}, {div} iterations, {mod} leftover")
            grid = history[previous + mod]
            break
        except ValueError:
            pass

    return sum(v == Acre.TREES for v in grid.values()) * sum(v == Acre.LUMBERYARD for v in grid.values())


test_content = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

assert part1(test_content) == 1147

with open("18.txt") as f:
    content = f.read()
print(part1(content))
print(part1(content, 1000000000))
