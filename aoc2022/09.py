from itertools import pairwise


def solve(content: str, *, part2: bool = False) -> int:
    rope = [0j] * (10 if part2 else 2)

    visited = set()
    for line in content.splitlines():
        direction, steps = line.split()
        for i in range(int(steps)):
            rope[0] += {"R": 1, "U": -1j, "L": -1, "D": 1j}[direction]

            for n, (head, tail) in enumerate(pairwise(rope), start=1):
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


assert (
    solve("""\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""")
    == 13
)
assert (
    solve(
        """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""",
        part2=True,
    )
    == 36
)

with open("09.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
