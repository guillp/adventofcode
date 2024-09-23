from collections import defaultdict
from itertools import combinations


def manhattan(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


def part1(content: str) -> int:
    points = {tuple(int(x) for x in line.split(",")) for line in content.strip().splitlines()}

    distances = defaultdict[tuple[int, ...], set[tuple[int, ...]]](set)
    for a, b in combinations(points, r=2):
        if manhattan(a, b) <= 3:
            distances[a].add(b)
            distances[b].add(a)

    constellations = set[frozenset[tuple[int, ...]]]()
    while points:
        starting_point = points.pop()
        constellation = {starting_point}
        remaining = {starting_point}
        while remaining:
            remaining |= distances[remaining.pop()] - constellation
            constellation |= remaining

        constellations.add(frozenset(constellation))
        points -= constellation

    return len(constellations)


assert (
    part1("""\
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0""")
    == 2
)

assert (
    part1("""\
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""")
    == 4
)


assert (
    part1("""\
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
""")
    == 3
)

assert (
    part1("""\
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
""")
    == 8
)

with open("25.txt") as f:
    content = f.read()
print(part1(content))
