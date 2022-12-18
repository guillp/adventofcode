from itertools import combinations

content = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

with open('18.txt') as finput: content = finput.read().strip()

cubes = {tuple(int(p) for p in line.split(',')) for line in content.splitlines()}


def surface_area(cubes: set[tuple[int, int, int]]) -> int:
    surface = len(cubes) * 6
    for (x1, y1, z1), (x2, y2, z2) in combinations(cubes, 2):
        if (
                x1 == x2 and y1 == y2 and abs(z1 - z2) == 1
                or x1 == x2 and abs(y1 - y2) == 1 and z1 == z2
                or abs(x1 - x2) == 1 and y1 == y2 and z1 == z2
        ):
            surface -= 2
    return surface


print(surface_area(cubes))


def exterior_surface_area(cubes: set[tuple[int, int, int]]) -> int:
    surface = surface_area(cubes)

    # build a rectangular volume completely surrounding the lava
    volume = {(x, y, z) for x in range(min(x for x, _, _ in cubes) - 1, max(x for x, _, _ in cubes) + 2)
              for y in range(min(y for _, y, _ in cubes) - 1, max(y for _, y, _ in cubes) + 2)
              for z in range(min(z for _, _, z in cubes) - 1, max(z for _, _, z in cubes) + 2)
              if (x, y, z) not in cubes}

    # then strip out the exterior
    to_visit = {(-1, -1, -1)} # this cube is always outside
    while to_visit:
        x, y, z = to_visit.pop()
        for c in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if c in volume:
                volume.remove(c)
                to_visit.add(c)

    # any cube left in volume is trapped inside the lava
    surface -= surface_area(volume)
    return surface


print(exterior_surface_area(cubes))
