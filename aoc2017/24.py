from heapq import heapify, heappop, heappush


def solve(content: str) -> tuple[int, int]:
    components = tuple(sorted(tuple(sorted(map(int, line.split("/")))) for line in content.strip().split()))

    pool: list[tuple[int, tuple[int, ...], int]] = [
        (sum(component), (i,), max(component)) for i, component in enumerate(components) if 0 in component
    ]
    heapify(pool)

    part1 = 0
    part2 = (0, 0)
    while pool:
        score, bridge, next_connector = heappop(pool)
        for i, (left, right) in enumerate(components):
            if i in bridge:
                continue  # don't use the same component twice
            if next_connector not in (left, right):
                continue  # next candidate doesn't have appropriate connector
            if left > next_connector:
                break  # avoid iterating over components with too many connectors
            next_score = score + left + right
            heappush(pool, (next_score, bridge + (i,), left if right == next_connector else right))
            part1 = max(part1, next_score)
            part2 = max(part2, (len(bridge) + 1, next_score))

    return part1, part2[1]


test_content = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
"""

assert solve(test_content) == (31, 19)

with open("24.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
