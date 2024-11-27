from itertools import combinations
from math import prod


def solve(content: str, *, part2: bool = False) -> int:
    all_numbers = tuple(int(x) for x in content.strip().splitlines())
    for numbers in combinations(all_numbers, r=3 if part2 else 2):
        if sum(numbers) == 2020:
            return prod(numbers)
    assert False, "solution not found"


test_content = """\
1721
979
366
299
675
1456
"""

assert solve(test_content) == 514579
assert solve(test_content, part2=True) == 241861950

with open("01.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
