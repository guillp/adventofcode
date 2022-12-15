content = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

with open("09.txt", "rt") as finput:
    content = finput.read()

rope = [0j] * 10

visited = set()
for line in content.splitlines():
    direction, steps = line.split()
    for i in range(int(steps)):
        rope[0] += {"R": 1, "U": -1j, "L": -1, "D": 1j}[direction]

        for n, (head, tail) in enumerate(zip(rope, rope[1:]), start=1):
            diff = head - tail
            if (
                abs(diff.real) > 1
                or abs(diff.imag) > 1
                or abs(diff.real) + abs(diff.imag) > 2
            ):
                if diff.real:
                    tail += 1 if diff.real > 0 else -1
                if diff.imag:
                    tail += 1j if diff.imag > 0 else -1j

            rope[n] = tail

            if n == len(rope) - 1:
                visited.add(tail)

print(len(visited))
