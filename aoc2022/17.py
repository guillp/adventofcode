from functools import cache
from itertools import cycle

content = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

with open("17.txt") as f:
    content = f.read().strip()

ROCKS = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


@cache
def move(rock: frozenset[complex], dir: complex):
    return frozenset(pos + dir for pos in rock)


def left(rock: frozenset[complex]) -> int:
    return int(min(pos.real for pos in rock))


def right(rock: frozenset[complex]) -> int:
    return int(max(pos.real for pos in rock))


def top(rock: frozenset[complex]) -> int:
    return int(min(pos.imag for pos in rock))


def bottom(rock: frozenset[complex]) -> int:
    return int(max(pos.imag for pos in rock))


rocks = [
    frozenset(
        complex(x + 2, -y - 4)  # adjusted so that rocks are at their starting positions
        for y, line in enumerate(reversed(rock_str.splitlines()))
        for x, c in enumerate(line)
        if c == "#"
    )
    for rock_str in ROCKS.strip().split("\n\n")
]

jets = cycle(content)


def print_chamber(chamber: set[complex], rock: frozenset[complex] | None = None):
    top_display = min(
        top(chamber),
        top(rock) if rock else 1,
    )
    for y in range(top_display, bottom(chamber)):
        print(
            "".join(
                "@"
                if rock and complex(x, y) in rock
                else "#"
                if complex(x, y) in chamber
                else "."
                for x in range(7)
            )
        )
    print()


def solve(n: int = 2022) -> int:
    chamber = frozenset(complex(i) for i in range(7))
    height = 0
    states = {}
    for i in range(n):
        rock = rocks[i % len(rocks)]

        # print_chamber(chamber, rock)
        while True:
            push = next(jets)
            pushed_rock = move(rock, -1 if push == "<" else 1)
            if (
                left(pushed_rock) >= 0
                and right(pushed_rock) < 7
                and not pushed_rock & chamber
            ):
                rock = pushed_rock

            fell_rock = move(rock, 1j)
            if not fell_rock & chamber:
                rock = fell_rock
            else:
                break

        chamber |= rock
        # keep only the top part of the chamber
        chamber = frozenset(pos for pos in chamber if pos.imag < 30)
        # calc how much the chamber has raised
        raised = -top(chamber)
        height += raised
        # put the chamber at 0 level again for the new rock
        chamber = move(chamber, raised * 1j)

        # print_chamber(chamber)

    return height


# print_chamber()
print(solve(2022))
