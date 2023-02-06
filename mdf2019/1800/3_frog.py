from collections import defaultdict
from itertools import combinations

n, d = (int(x) for x in input().split())
x, y = (int(x) for x in input().split())
start = complex(x, y)

lillies = set()
for _ in range(n):
    x, y = (int(x) for x in input().split())
    lillies.add(complex(x, y))


def dist(a: complex, b: complex) -> float:
    return ((a - b).real ** 2 + (a - b).imag ** 2) ** .5


G = defaultdict(set)
for a, b in combinations(lillies, 2):
    if dist(a, b) <= d:
        G[a].add(b)
        G[b].add(a)

for a in lillies:
    if dist(start, a) <= d:
        G[start].add(a)
        G[a].add(start)


def dfs(G, *path):
    next_steps = G[path[-1]] - set(path)
    if next_steps:
        for step in next_steps:
            yield from dfs(G, *path, step)
    else:
        yield path


all_paths = [*dfs(G, start)]
print(max(len(path) for path in all_paths) - 1)
