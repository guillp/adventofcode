from collections.abc import Iterator
from itertools import combinations


def solve(content: str, nb_connections: int) -> Iterator[int]:
    boxes = {tuple(map(int, line.split(","))) for line in content.strip().splitlines()}
    distances = sorted([(sum((x - y) ** 2 for x, y in zip(a, b)), a, b) for a, b in combinations(boxes, 2)])

    connections = {box: {box} for box in boxes}
    for i, (distance, a, b) in enumerate(distances):
        connections[a].update(connections[b])
        if connections[a] == boxes:  # all boxes connected together, yield part2
            yield a[0] * b[0]
            return
        for box in connections[a]:  # points all boxes to the same circuit
            connections[box] = connections[a]
        if i == nb_connections - 1:  # once we made the required number of connections, yield part1
            circuits = sorted({frozenset(circuit) for circuit in connections.values()}, key=lambda c: len(c))
            yield len(circuits[-1]) * len(circuits[-2]) * len(circuits[-3])


test_content = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

assert tuple(solve(test_content, 10)) == (40, 25272)

with open("08.txt") as f:
    content = f.read()

for part in solve(content, 1000):
    print(part)
