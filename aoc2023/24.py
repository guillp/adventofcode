import re
from contextlib import suppress
from itertools import combinations


def part1(content: str, area_min: int = 7, area_max: int = 28) -> int:
    hails = [tuple(int(x) for x in re.findall(r"-?\d+", line)) for line in content.splitlines()]
    intersections = 0
    for (x1, y1, z1, vx1, vy1, vz1), (x2, y2, z2, vx2, vy2, vz2) in combinations(hails, 2):
        with suppress(ZeroDivisionError):
            # time of intersection
            t1 = ((y2 - y1) * vx2 - (x2 - x1) * vy2) / (vx2 * vy1 - vy2 * vx1)
            t2 = ((y2 - y1) * vx1 - (x2 - x1) * vy1) / (vx2 * vy1 - vy2 * vx1)

            x = x1 + vx1 * t1  # intersection X
            y = y1 + vy1 * t1  # intersection Y
            if t1 > 0 and t2 > 0 and area_min <= x <= area_max and area_min <= y <= area_max:
                intersections += 1

    return intersections


from z3 import Int, Ints, Solver, sat


def part2(content: str) -> int:
    hails = [tuple(int(x) for x in re.findall(r"-?\d+", line)) for line in content.splitlines()]

    # use Z3, it is the closest thing to magic!
    s = Solver()
    # the coordinates and throw velocity we are looking for
    xt, yt, zt, vxt, vyt, vzt = Ints("x y z vx vy vz")

    # add the constraint that must be met for each hail
    for i, (x, y, z, vx, vy, vz) in enumerate(hails):
        time = Int(f"t{i}")
        s.add(
            xt + time * vxt == x + vx * time,
            yt + time * vyt == y + vy * time,
            zt + time * vzt == z + vz * time,
        )

    # let Z3 deduce everything
    assert s.check() == sat
    m = s.model()
    return m[xt].as_long() + m[yt].as_long() + m[zt].as_long()  # type: ignore[no-any-return]


test_content = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

assert part1(test_content, area_min=7, area_max=28) == 2
assert part2(test_content) == 47

with open("24.txt") as f:
    content = f.read()

print(part1(content, area_min=200000000000000, area_max=400000000000000))
print(part2(content))
