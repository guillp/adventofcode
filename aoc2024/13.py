import math
import re
from contextlib import suppress


def optimize(xa: int, ya: int, xb: int, yb: int, xt: int, yt: int) -> tuple[int, int]:  # noqa: PLR0913
    # we know that `A * xa + B * xb = xt` and `A * ya + B * yb = yt`.
    # so B = (xt - A * xa) / xb
    # replace B in the second equation: A * ya + (xt - A * xa) / xb * yb = yt
    # so A = (yt - xt * yb / xb) / (ya - xa * yb / xb)

    top = yt - xt * yb / xb
    bottom = ya - xa * yb / xb

    a, mod = divmod(top, bottom)
    # due to floating point precision, we need to check if the result is close to an integer
    if math.isclose(mod, 0, abs_tol=1e-2):
        mod = 0
    if mod != 0 and math.isclose(bottom - mod, 0, abs_tol=1e-2):
        a += 1
        mod = 0
    if mod == 0:
        b = (xt - a * xa) / xb
        return int(a), int(b)

    raise ValueError("Solution not found!")


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for machine in content.split("\n\n"):
        xa, ya, xb, yb, xt, yt = map(int, re.findall(r"(\d+)", machine, re.MULTILINE))
        with suppress(ValueError):
            a, b = optimize(xa, ya, xb, yb, xt, yt)
            part1 += a * 3 + b

        with suppress(ValueError):
            a, b = optimize(xa, ya, xb, yb, xt + 10000000000000, yt + 10000000000000)
            assert a * xa + b * xb == xt + 10000000000000
            assert a * ya + b * yb == yt + 10000000000000
            part2 += a * 3 + b

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
