from itertools import combinations
from math import prod


def solve(content: str, part2: bool = False) -> int:
    weights = [int(line) for line in content.splitlines()]

    total_weight = sum(weights)
    group1 = min(
        (
            comb
            for i in range(len(weights))
            for comb in combinations(weights, i)
            if sum(comb) == total_weight // (4 if part2 else 3)
        ),
        key=prod,
    )
    return prod(group1)


with open("24.txt") as finput:
    content = finput.read()

print(solve(content))
print(solve(content, part2=True))
