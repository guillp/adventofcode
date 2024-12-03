import re
from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    yield sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d+),(\d+)\)", content, re.MULTILINE))

    part2 = 0
    enabled = True
    for instruction in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", content):
        match instruction:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case mul if enabled:
                a, b = (int(x) for x in re.findall(r"\d+", mul))
                part2 += a * b

    yield part2


assert next(solve("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))")) == 161
assert tuple(solve("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"))[1] == 48

with open("03.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
