from collections.abc import Iterator
from itertools import combinations


def solve(content: str) -> Iterator[int]:
    TARGET = 150
    containers = tuple(sorted(int(x) for x in content.splitlines()))

    yield sum(sum(comb) == TARGET for i in range(len(containers)) for comb in combinations(containers, i))
    m = min(i for i in range(len(containers)) for comb in combinations(containers, i) if sum(comb) == TARGET)
    yield sum(sum(comb) == TARGET for comb in combinations(containers, m))


with open("17.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
