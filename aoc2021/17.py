import re
from collections.abc import Iterator
from itertools import count, takewhile


def shoot(x: int, y: int) -> Iterator[tuple[int, int]]:
    for n in count():
        yield sum(range(max(x - n + 1, 0), x + 1)), y * n - n * (n - 1) // 2


def solve(content: str) -> Iterator[int]:
    xmin, xmax, ymin, ymax = (int(x) for x in re.findall(r"-?\d+", content))

    # We launch the probe upwards with a vertical velocity of yv that must be the highest possible.
    # yx decreases by 1 every step.
    # At its highest y position, the probe has a vertical velocity of 0.
    # It then accelerates downwards by 1 every step.
    # It eventually comes back to y=0 with a velocity of -yv.
    # Its next step will put the probe at -yv-1 units.
    # For its next step to be within our target range, -yv-1 must be equal to ymin.
    # so -yv-1 = ymin => yv = -ymin-1
    # when it reaches its peak, probe will be at (-ymin-1)*(-ymin-1+1)/2 units which is equal to ymin*(ymin+1)/2

    yield ymin * (ymin + 1) // 2

    solutions = {
        (xv, yv)
        for yv in range(ymin, -ymin + 1)
        for xv in range(1, xmax + 1)
        if any(xmin <= x <= xmax and ymin <= y <= ymax for x, y in takewhile(lambda xy: xy[1] >= ymin, shoot(xv, yv)))
    }
    yield len(solutions)


assert tuple(solve("target area: x=20..30, y=-10..-5")) == (45, 112)


with open("17.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
