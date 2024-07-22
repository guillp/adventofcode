def part1(content: str) -> int:
    rope = [0j] * 10

    visited = set()
    for line in content.splitlines():
        direction, steps = line.split()
        for _ in range(int(steps)):
            rope[0] += {"R": 1, "U": -1j, "L": -1, "D": 1j}[direction]

            for n, (head, tail) in enumerate(zip(rope, rope[1:]), start=1):
                diff = head - tail
                if abs(diff.real) > 1 or abs(diff.imag) > 1 or abs(diff.real) + abs(diff.imag) > 2:
                    if diff.real:
                        tail += 1 if diff.real > 0 else -1
                    if diff.imag:
                        tail += 1j if diff.imag > 0 else -1j

                rope[n] = tail

                if n == len(rope) - 1:
                    visited.add(tail)

    return len(visited)


test_content = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

print(part1(test_content))

with open("09.txt") as f:
    content = f.read()

print(part1(content))
