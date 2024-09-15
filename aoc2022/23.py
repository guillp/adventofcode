from collections import defaultdict, deque
from collections.abc import Iterator
from functools import cache

NORTH, SOUTH, EAST, WEST = -1j, 1j, 1, -1

DIRECTIONS = deque(
    (
        (NORTH, {NORTH + EAST, NORTH, NORTH + WEST}),
        (SOUTH, {SOUTH + EAST, SOUTH, SOUTH + WEST}),
        (WEST, {WEST + NORTH, WEST, WEST + SOUTH}),
        (EAST, {EAST + NORTH, EAST, EAST + SOUTH}),
    ),
)


def solve(content: str) -> Iterator[int]:
    @cache
    def elves_at(m: int) -> set[complex]:
        if m == 0:
            return {
                complex(x, y) for y, line in enumerate(content.splitlines()) for x, c in enumerate(line) if c == "#"
            }

        previous_elves = elves_at(m - 1)

        directions = DIRECTIONS.copy()
        directions.rotate(-m + 1)

        moves = defaultdict(set)
        new_elves = set()
        for pos in previous_elves:
            if not any(
                pos + d in previous_elves
                for d in (
                    NORTH,
                    NORTH + EAST,
                    EAST,
                    SOUTH + EAST,
                    SOUTH,
                    SOUTH + WEST,
                    WEST,
                    NORTH + WEST,
                )
            ):
                new_elves.add(pos)
                continue
            for direction, tests in directions:
                if not any(pos + test in previous_elves for test in tests):
                    moves[pos + direction].add(pos)
                    break
            else:
                new_elves.add(pos)

        for new_pos, elves in moves.items():
            if len(elves) == 1:
                new_elves.add(new_pos)
            else:
                new_elves |= elves

        assert len(new_elves) == len(previous_elves)
        return new_elves

    # print_elves(elves_at(10))
    yield score(elves_at(10))

    i = 1
    while elves_at(i) != elves_at(i + 1):
        i += 1

    yield i + 1


def print_elves(elves: set[complex]) -> None:
    min_x = int(min(pos.real for pos in elves))
    max_x = int(max(pos.real for pos in elves))
    min_y = int(min(pos.imag for pos in elves))
    max_y = int(max(pos.imag for pos in elves))

    for y in range(min_y, max_y + 1):
        print("".join("#" if complex(x, y) in elves else "." for x in range(min_x, max_x + 1)))
    print()


def score(elves: set[complex]) -> int:
    min_x = int(min(pos.real for pos in elves))
    max_x = int(max(pos.real for pos in elves))
    min_y = int(min(pos.imag for pos in elves))
    max_y = int(max(pos.imag for pos in elves))

    return (max_y - min_y + 1) * (max_x - min_x + 1) - len(elves)


test_content = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
"""

assert tuple(solve(test_content)) == (110, 20)

with open("23.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
