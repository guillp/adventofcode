import re
from collections import defaultdict
from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    distances: dict[str, dict[str, int]] = defaultdict(dict)
    for start, stop, cost in re.findall(r"(\w+) to (\w+) = (\d+)", content, re.MULTILINE):
        distances[start][stop] = int(cost)
        distances[stop][start] = int(cost)

    all_locations = frozenset(start for start in distances)

    pool: set[tuple[tuple[str, ...], frozenset[str], int]] = {
        ((start,), all_locations - {start}, 0) for start in distances
    }

    best_path = sum(cost for stops in distances.values() for cost in stops.values())

    while pool:
        path, remaining, cost = max(pool, key=lambda x: (len(x[0]), -x[2]))
        pool.remove((path, remaining, cost))
        if cost > best_path:
            continue
        if remaining:
            for next_location in remaining:
                if new_cost := distances.get(path[-1], {}).get(next_location):
                    next_cost = cost + new_cost
                    if next_cost > best_path:
                        continue
                    next_remaining = remaining - {next_location}
                    if next_remaining:
                        pool.add(((*path, next_location), next_remaining, next_cost))
                    elif next_cost < best_path:
                        best_path = next_cost
    yield best_path

    part2 = best_path
    pool = {((start,), all_locations - {start}, 0) for start in distances}
    while pool:
        path, remaining, cost = max(pool, key=lambda x: (len(x[0]), x[2]))
        pool.remove((path, remaining, cost))
        if remaining:
            for next_location in remaining:
                if new_cost := distances.get(path[-1], {}).get(next_location):
                    next_cost = cost + new_cost
                    next_remaining = remaining - {next_location}
                    if next_remaining:
                        pool.add(((*path, next_location), next_remaining, next_cost))
                    elif next_cost > part2:
                        part2 = next_cost

    yield part2


test_content = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

# assert tuple(solve(test_content)) == (605, 982)
with open("09.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
