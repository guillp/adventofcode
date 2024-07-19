import math
import re
from itertools import combinations


def solve(content: str, steps: int = 1000) -> tuple[int, int | None]:
    pos = [
        [int(x), int(y), int(z)] for x, y, z in re.findall(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", content, re.MULTILINE)
    ]
    nb_moons = len(pos)
    pos0 = tuple(list(p) for p in pos)
    vel = [[0, 0, 0] for _ in pos]
    loops: list[int | None] = [None, None, None]

    for step in range(1, 100000000):
        # apply gravity
        for a, b in combinations(range(nb_moons), 2):
            for i, (pa, pb) in enumerate(zip(pos[a], pos[b])):
                if pa < pb:
                    vel[a][i] += 1
                    vel[b][i] -= 1
                elif pa > pb:
                    vel[b][i] += 1
                    vel[a][i] -= 1
        # apply velocity
        for i in range(nb_moons):
            for axis in (0, 1, 2):
                pos[i][axis] += vel[i][axis]

        # part 1
        if step == steps:
            yield sum(sum(abs(x) for x in p) * sum(abs(x) for x in v) for p, v in zip(pos, vel))

        # part 2: check for loops
        for axis in (0, 1, 2):  # for each axis
            # check that velocities on that axis are all 0
            if all(vel[moon][axis] == 0 for moon in range(nb_moons)):
                # check that positions on that axis are same as initial
                if all(pos[moon][axis] == pos0[moon][axis] for moon in range(nb_moons)):
                    if loops[axis] is None:  # keep only the smallest cycle
                        loops[axis] = step

                if None not in loops:
                    yield math.lcm(*loops)
                    return


assert tuple(
    solve(
        """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""",
        100,
    )
) == (1940, 4686774924)


with open("12.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
