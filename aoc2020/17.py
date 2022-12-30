from functools import cache
from typing import Iterable

content = """.#.
..#
###
"""

with open("17.txt") as f:
    content = f.read()


def neighbors(x: int, y: int, z: int):
    return (
        (x + xd, y + yd, z + zd)
        for xd in (-1, 0, 1)
        for yd in (-1, 0, 1)
        for zd in (-1, 0, 1)
        if not xd == yd == zd == 0
    )


def surround(cubes: set[tuple[int, int, int]]) -> Iterable[tuple[int, int, int]]:
    min_x = max_x = min_y = max_y = min_z = max_z = 0
    for x, y, z in cubes:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                yield x, y, z, (x, y, z) in cubes


@cache
def cubes_at_cycle(cycle: int) -> set[tuple[int, int, int]]:
    if cycle == 0:
        return {
            (x, y, 0)
            for y, line in enumerate(content.splitlines())
            for x, c in enumerate(line)
            if c == "#"
        }
    previous_cubes = cubes_at_cycle(cycle - 1)
    new_cubes = set()
    for x, y, z, state in surround(previous_cubes):
        if state:
            if sum(nb in previous_cubes for nb in neighbors(x, y, z)) in (2, 3):
                new_cubes.add((x, y, z))
        else:
            if sum(nb in previous_cubes for nb in neighbors(x, y, z)) == 3:
                new_cubes.add((x, y, z))

    return new_cubes


print(len(cubes_at_cycle(6)))


def hyperneighbors(w: int, x: int, y: int, z: int):
    return (
        (w + wd, x + xd, y + yd, z + zd)
        for wd in (-1, 0, 1)
        for xd in (-1, 0, 1)
        for yd in (-1, 0, 1)
        for zd in (-1, 0, 1)
        if not wd == xd == yd == zd == 0
    )


def hypersurround(
    cubes: set[tuple[int, int, int, int]]
) -> Iterable[tuple[int, int, int]]:
    min_w = max_w = min_x = max_x = min_y = max_y = min_z = max_z = 0
    for w, x, y, z in cubes:
        min_w = min(min_w, w)
        max_w = max(max_w, w)
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)
    for w in range(min_w - 1, max_w + 2):
        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                for z in range(min_z - 1, max_z + 2):
                    yield w, x, y, z, (w, x, y, z) in cubes


@cache
def hypercubes_at_cycle(cycle: int) -> set[tuple[int, int, int, int]]:
    if cycle == 0:
        return {
            (0, x, y, 0)
            for y, line in enumerate(content.splitlines())
            for x, c in enumerate(line)
            if c == "#"
        }
    previous_cubes = hypercubes_at_cycle(cycle - 1)
    new_cubes = set()
    for w, x, y, z, state in hypersurround(previous_cubes):
        if state:
            if sum(nb in previous_cubes for nb in hyperneighbors(w, x, y, z)) in (2, 3):
                new_cubes.add((w, x, y, z))
        else:
            if sum(nb in previous_cubes for nb in hyperneighbors(w, x, y, z)) == 3:
                new_cubes.add((w, x, y, z))

    return new_cubes


print(len(hypercubes_at_cycle(6)))
