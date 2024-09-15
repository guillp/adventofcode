import re
from collections.abc import Iterator

from z3 import Bool, If, Int, Ints, Optimize  # type: ignore[import-untyped]


def solve(content: str) -> Iterator[int]:
    def iter_bots() -> Iterator[tuple[tuple[int, int, int], int]]:
        for line in content.strip().splitlines():
            x, y, z, r = map(int, re.findall(r"-?\d+", line))
            yield (x, y, z), r

    bots = dict(iter_bots())
    nbots = len(bots)

    strongest = max(bots, key=lambda bot: bots[bot])
    rng = bots[strongest]

    yield sum(sum(abs(a - b) for a, b in zip(bot, strongest)) <= rng for bot in bots)

    # z3 to the rescue
    o = Optimize()
    x, y, z = Ints("x y z")

    def Abs(x: Int) -> If:  # noqa: N802
        return If(x >= 0, x, -x)

    is_in_range = [Bool(f"in_range{i}") for i in range(nbots)]

    for i, ((bx, by, bz), rng) in enumerate(bots.items()):
        o.add(is_in_range[i] == (Abs(x - bx) + Abs(y - by) + Abs(z - bz) <= rng))
    bots_in_range = Int("n")
    o.add(bots_in_range == sum(is_in_range))

    distance = Int("d")
    o.add(distance == Abs(x) + Abs(y) + Abs(z))

    o.maximize(bots_in_range)
    o.minimize(distance)

    assert o.check()
    m = o.model()
    yield abs(m[x].as_long()) + abs(m[y].as_long()) + abs(m[z].as_long())


test_content = """\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
"""

assert tuple(solve(test_content)) == (7, 1)

with open("23.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
