import re
from itertools import product

from z3 import Ints, Optimize, sat  # type: ignore[import-untyped]


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for machine in content.split("\n\n"):
        xa, ya, xb, yb, xt, yt = map(int, re.findall(r"(\d+)", machine, re.MULTILINE))
        part1 += min(
            (a * 3 + b for a, b in product(range(100), repeat=2) if a * xa + b * xb == xt and a * ya + b * yb == yt),
            default=0,
        )

        a, b = Ints("a b")
        o = Optimize()
        o.add(a * xa + b * xb == xt + 10_000_000_000_000)
        o.add(a * ya + b * yb == yt + 10_000_000_000_000)
        o.add(a >= 0)
        o.add(b >= 0)
        o.minimize(a + b)
        if o.check() == sat:
            m = o.model()
            part2 += m[a].as_long() * 3 + m[b].as_long()

    return part1, part2


test_content = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

assert solve(test_content)[0] == 480

with open("13.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
