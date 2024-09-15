import math
from collections.abc import Iterator
from itertools import combinations


def solve(content: str) -> Iterator[int]:
    asteroids = {(x, y) for y, line in enumerate(content.splitlines()) for x, c in enumerate(line) if c == "#"}

    # assume every asteroid sees each other for now
    los = {a: set(asteroids) - {a} for a in asteroids}

    # now check for asteroids that hide others
    for (xa, ya), (xb, yb), (xc, yc) in combinations(sorted(asteroids), 3):
        # check if the 3 points are aligned
        if (yb - ya) * (xc - xb) == (yc - yb) * (xb - xa):
            los[xa, ya] -= {(xc, yc)}
            los[xc, yc] -= {(xa, ya)}

    best_x, best_y = max(los, key=lambda a: len(los[a]))
    yield len(los[best_x, best_y])

    def angle(xy: tuple[int, int]) -> float:
        x, y = xy
        return -math.atan2(x - best_x, y - best_y) + math.pi / 4

    if len(los) >= 200:
        x200, y200 = sorted(los[best_x, best_y], key=angle)[199]
        yield x200 * 100 + y200


assert (
    next(
        solve("""\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""),
    )
    == 33
)


assert (
    next(
        solve("""\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""),
    )
    == 35
)

assert (
    next(
        solve("""\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""),
    )
    == 41
)

assert tuple(
    solve("""\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""),
) == (210, 802)

with open("10.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
