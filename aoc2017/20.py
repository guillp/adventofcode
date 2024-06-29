import re
from collections import defaultdict
from collections.abc import Iterator


def part1(content: str) -> int:
    def iter_particles() -> Iterator[tuple[int, int, int, int]]:
        for i, line in enumerate(content.splitlines()):
            # note that \d+ will read only absolute values, ignoring character "-"
            px, py, pz, vx, vy, vz, ax, ay, az = map(int, re.findall(r"\d+", line))
            yield ax + ay + az, vx + vy + vz, px + py + pz, i

    particles = sorted(iter_particles())
    return particles[0][3]  # the particle with the lowest acceleration, lowest speed and closed position to 0


def part2(content: str, ticks: int = 1000) -> int:
    def iter_particles() -> Iterator[tuple[tuple[int, int, int], tuple[tuple[int, int, int], tuple[int, int, int]]]]:
        for i, line in enumerate(content.splitlines()):
            px, py, pz, vx, vy, vz, ax, ay, az = map(int, re.findall(r"-?\d+", line))
            yield (px, py, pz), ((ax, ay, az), (vx, vy, vz))

    particles = dict(iter_particles())
    for tick in range(1, ticks + 2):
        collisions: dict[tuple[int, int, int], int] = defaultdict(int)
        new_particles = {}
        for (px, py, pz), ((ax, ay, az), (vx, vy, vz)) in particles.items():
            pos = (px + vx + ax * tick), (py + vy + ay * tick), (pz + vz + az * tick)
            collisions[pos] += 1
            new_particles[pos] = ((ax, ay, az), (vx, vy, vz))
        for pos, col in collisions.items():
            if col > 1:
                del new_particles[pos]
        particles = new_particles

    return len(particles)


with open("20.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
