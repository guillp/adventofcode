import re
from collections import defaultdict


def solve(content: str) -> tuple[int, int]:
    G = defaultdict(set)
    for line in content.strip().splitlines():
        src, *dsts = map(int, re.findall(r"\d+", line))
        G[src].update(dsts)
        for dst in dsts:
            G[dst].add(src)

    remaining = set(G)
    groups = {}
    while remaining:
        next_group = min(remaining)
        connected = {next_group}
        verified: set[int] = set()
        while verified != connected:
            for program in connected - verified:
                connected |= G[program]
                verified.add(program)
        groups[next_group] = connected
        remaining -= connected

    return len(groups[0]), len(groups)


test_content = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""

assert solve(test_content) == (6, 2)

with open("12.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
