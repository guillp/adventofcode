import re

from z3 import Solver, Int, sat
test_content = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

with open("15.txt") as f:
    content = f.read()


def part1(content: str) -> int:
    s = Solver()
    t = Int("t")
    s.add(t>=0)
    for line in content.splitlines():
        disc, positions, _, initial_pos = re.findall(r"\d+", line)
        s.add((initial_pos + t+disc) % positions == 0)

    if s.check() == sat:
        m = s.model()
        return m[t].as_long()

assert part1(test_content) == 5
print(part1(content))


def part2(content: str) -> int:
    lines = content.splitlines()
    return part1(content+f"Disc #{len(lines)+1} has 11 positions; at time=0, it is at position 0.")

print(part2(content))