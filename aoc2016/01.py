from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    pos, angle = 0j, 1 + 0j
    visited: set[complex] = {0}
    part2: int | None = None
    for instruction in content.split(", "):
        direction, steps = instruction[0], instruction[1:]
        angle *= {"L": 1j, "R": -1j}[direction]
        for _ in range(int(steps)):
            pos += angle
            if pos in visited and part2 is None:
                part2 = int(abs(pos.real) + abs(pos.imag))
            visited.add(pos)
    yield int(abs(pos.real) + abs(pos.imag))
    if part2 is not None:
        yield part2


with open("01.txt") as finput:
    content = finput.read()

for part in solve(content):
    print(part)
