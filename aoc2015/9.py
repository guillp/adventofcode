from collections import defaultdict

from stringparser import Parser

with open('9.txt', "rt") as finput:
    content = finput.read()


parser = Parser("{} to {} = {:d}")
distances = defaultdict(dict)
for line in content.splitlines():
    start, stop, cost = parser(line)
    distances[start][stop] = cost
    distances[stop][start] = cost

all_locations = frozenset(start for start in distances)

pool = {((start,), all_locations - {start}, 0) for start in distances}

m = sum(cost for stops in distances.values() for cost in stops.values())
while pool:
    path, remaining, cost = max(pool, key=lambda x: (len(x[0]), -x[2]))
    pool.remove((path, remaining, cost))
    if cost > m:
        continue
    if remaining:
        for next_location in remaining:
            if new_cost := distances.get(path[-1], {}).get(next_location):
                next_cost = cost + new_cost
                if next_cost > m:
                    continue
                next_remaining = remaining - {next_location}
                if next_remaining:
                    pool.add((path + (next_location,), next_remaining, next_cost))
                elif next_cost < m:
                    m = next_cost

print(m)

pool = {((start,), all_locations - {start}, 0) for start in distances}

m2 = m
while pool:
    path, remaining, cost = max(pool, key=lambda x: (len(x[0]), x[2]))
    pool.remove((path, remaining, cost))
    if remaining:
        for next_location in remaining:
            if new_cost := distances.get(path[-1], {}).get(next_location):
                next_cost = cost + new_cost
                next_remaining = remaining - {next_location}
                if next_remaining:
                    pool.add((path + (next_location,), next_remaining, next_cost))
                elif next_cost > m2:
                    m2 = next_cost

print(m2)
