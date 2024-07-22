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


def move(rock: frozenset[complex], direction: complex) -> frozenset[complex]:
    return frozenset(pos + direction for pos in rock)


rocks = [
    frozenset(
        complex(x + 2, -y - 4)  # adjusted so that rocks are at their starting positions
        for y, line in enumerate(reversed(rock_str.splitlines()))
        for x, c in enumerate(line)
        if c == "#"
    )
    for rock_str in ROCKS.strip().split("\n\n")
]


def print_chamber(chamber: set[complex], rock: frozenset[complex] | None = None) -> None:
    top_display = int(min(
        min(pos.imag for pos in chamber),
        min(pos.imag for pos in rock) if rock else 1,
    ))
    for y in range(top_display, 50):
        print(
            "".join(
                "@" if rock and complex(x, y) in rock else "#" if complex(x, y) in chamber else "." for x in range(7)
            )
        )
    print()


def solve(content: str, n: int) -> int:
    chamber = frozenset(complex(i) for i in range(7))
    height = 0
    jet = 0
    i = 0
    states: dict[tuple[int, int, frozenset[complex]], tuple[int, int]] = {}
    while i < n:
        # loop detection, when we end up in a previously known state
        state = (i % len(rocks), jet, chamber)
        if state in states:
            j, h = states[state]
            loops, remaining = divmod(n - j, i - j)
            height += (height - h) * (loops - 1)
            i = n - remaining

        rock = rocks[i % len(rocks)]
        while True:
            pushed_rock = move(rock, -1 if content[jet] == "<" else 1)
            jet += 1
            jet %= len(content)
            if (
                min(pos.real for pos in pushed_rock) >= 0
                and max(pos.real for pos in pushed_rock) < 7
                and not pushed_rock & chamber
            ):
                rock = pushed_rock

            fell_rock = move(rock, 1j)
            if not fell_rock & chamber:
                rock = fell_rock
            else:
                break

        chamber |= rock
        # keep only the top part of the chamber, using an arbitrary large value (result from part1)
        chamber = frozenset(pos for pos in chamber if pos.imag < 3068)
        # calc how much the chamber has raised
        raised = -int(min(pos.imag for pos in chamber))
        height += raised
        # put the chamber at 0 level again for the new rock
        chamber = move(chamber, raised * 1j)

        states[state] = (i, height)
        i += 1
        # print_chamber(chamber)

    return height


test_content = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

assert solve(test_content, 2022) == 3068
#assert solve(test_content, 1_000_000_000_000) == 1514285714288  #TODO: fix this

with open("17.txt") as f:
    content = f.read().strip()

print(solve(content, 2022))
print(solve(content, 1_000_000_000_000))
