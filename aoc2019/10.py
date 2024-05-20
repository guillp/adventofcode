import math
from itertools import combinations


def solve(content: str) -> tuple[int, int | None]:
    asteroids = {
        (x, y)
        for y, line in enumerate(content.splitlines())
        for x, c in enumerate(line)
        if c == "#"
    }

    # assume every asteroid sees each other for now
    los = {a: set(asteroids) - {a} for a in asteroids}

    # now check for asteroids that hide others
    for (xa, ya), (xb, yb), (xc, yc) in combinations(sorted(asteroids), 3):
        # check if the 3 points are aligned
        if (yb - ya) * (xc - xb) == (yc - yb) * (xb - xa):
            los[xa, ya] -= {(xc, yc)}
            los[xc, yc] -= {(xa, ya)}

    best_x, best_y = max(los, key=lambda a: len(los[a]))
    part1 = len(los[best_x, best_y])

    def angle(xy) -> float:
        x, y = xy
        return -math.atan2(x - best_x, y - best_y) + math.pi / 4

    part2 = None
    if len(los) >= 200:
        x200, y200 = sorted(los[best_x, best_y], key=angle)[199]
        part2 = x200 * 100 + y200

    return part1, part2


assert solve("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""") == (33, None)


assert solve("""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""") == (35, None)

assert solve(""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""") == (41, None)

assert solve(""".#..##.###...#######
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
###.##.####.##.#..##""") == (210, 802)

with open("10.txt") as f:
    content = f.read()

print(*solve(content), sep="\n")
