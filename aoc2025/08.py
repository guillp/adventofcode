from itertools import combinations


def solve(content: str, nb_connections: int) -> tuple[int, int]:
    boxes = {tuple(map(int, line.split(","))) for line in content.strip().splitlines()}
    distances = sorted([(sum((x - y) ** 2 for x, y in zip(a, b)), a, b) for a, b in combinations(boxes, 2)])

    connections = {box: {box} for box in boxes}
    for distance, a, b in distances[:nb_connections]:
        connections[a].update(connections[b])
        for box in connections[a]:
            connections[box] = connections[a]

    circuits = sorted({frozenset(circuit) for circuit in connections.values()}, key=lambda c: len(c), reverse=True)
    part1 = len(circuits[0]) * len(circuits[1]) * len(circuits[2])

    for distance, a, b in distances[nb_connections:]:
        connections[a].update(connections[b])
        if connections[a] == boxes:
            return part1, a[0] * b[0]
        for box in connections[a]:
            connections[box] = connections[a]

    assert False


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

assert solve(test_content, 10) == (40, 25272)

with open("08.txt") as f:
    content = f.read()

for part in solve(content, 1000):
    print(part)
