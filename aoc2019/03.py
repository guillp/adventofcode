content = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""

with open("03.txt") as f:
    content = f.read()

first_path, second_path = content.splitlines()


def wire(path: str) -> set[complex]:
    wire = {}
    pos = 0j
    steps = 0
    for step in path.split(","):
        direction = step[0]
        count = int(step[1:])
        d = {"R": 1, "D": 1j, "U": -1j, "L": -1}[direction]
        for i in range(1, count + 1):
            pos += d
            steps += 1
            wire.setdefault(pos, steps)
    return wire


first_wire = wire(first_path)
second_wire = wire(second_path)
intersections = set(first_wire) & set(second_wire)

print(min(map(lambda p: int(abs(p.real) + abs(p.imag)), intersections)))

print(min(map(lambda p: first_wire[p] + second_wire[p], intersections)))
