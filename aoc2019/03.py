from collections.abc import Iterator


def wire(path: str) -> dict[complex, int]:
    wire: dict[complex, int] = {}
    pos = 0j
    steps = 0
    for step in path.split(","):
        direction = step[0]
        count = int(step[1:])
        d = {"R": 1, "D": 1j, "U": -1j, "L": -1}[direction]
        for _ in range(1, count + 1):
            pos += d
            steps += 1
            wire.setdefault(pos, steps)
    return wire


def solve(content: str) -> Iterator[int]:
    first_path, second_path = content.splitlines()

    first_wire = wire(first_path)
    second_wire = wire(second_path)
    intersections = set(first_wire) & set(second_wire)

    yield min(int(abs(p.real) + abs(p.imag)) for p in intersections)
    yield min(first_wire[p] + second_wire[p] for p in intersections)


assert tuple(
    solve("""\
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""),
) == (159, 610)
assert tuple(
    solve("""\
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""),
) == (135, 410)

with open("03.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
