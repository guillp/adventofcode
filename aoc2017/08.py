import operator
from collections import defaultdict


def solve(content: str) -> tuple[int, int]:
    registers: dict[str, int] = defaultdict(int)
    part2 = 0
    for line in content.splitlines():
        reg, op, val, _, testreg, testop, testval = line.split()

        testmeth = {
            ">": operator.gt,
            "<": operator.lt,
            "<=": operator.le,
            ">=": operator.ge,
            "==": operator.eq,
            "!=": operator.ne,
        }[testop]
        if testmeth(registers[testreg], int(testval)):
            registers[reg] += int(val) * (1 if op == "inc" else -1)
        part2 = max(part2, max(registers.values()))

    return max(registers.values()), part2


test_content = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""

assert solve(test_content) == (1, 10)

with open("08.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
