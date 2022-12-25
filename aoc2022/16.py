import itertools
from operator import itemgetter

from stringparser import Parser

content = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

with open("16.txt", "rt") as finput:
    content = finput.read()

parser = Parser("Valve {} ha flow rate={:d}; tunnel lead to valve {}")
G = {}
flows = {}
for line in content.splitlines():
    name, flow, next_valves = parser(line.replace("s", ""))
    G[name] = {valve: 1 for valve in next_valves.split(", ")}
    flows[name] = flow

for k, i, j in itertools.permutations(G, 3):
    G[i][j] = min(G[i].get(j, len(G)), G[i].get(k, len(G)) + G[k].get(j, len(G)))

valves_to_open = {valve for valve, flow in flows.items() if flow > 0}


def dfs(pressure, valves_to_open, time, *path):
    yield pressure, path
    current_valve = path[-1]
    for next_valve in valves_to_open:
        distance = G[current_valve][next_valve]
        if time - distance - 1 > 0:
            yield from dfs(
                pressure + (time - distance - 1) * flows[next_valve],
                valves_to_open - {next_valve},
                time - distance - 1,
                *path,
                next_valve,
            )


best_pressure, best_path = max(dfs(0, valves_to_open, 30, "AA"), key=itemgetter(0))
print(best_pressure)
print(best_path)

s2 = 0
my_best_path = elephant_best_path = None
for my_part in itertools.combinations(valves_to_open, len(valves_to_open) // 2):
    my_pressure, my_path = max(dfs(0, set(my_part), 26, "AA"), key=itemgetter(0))
    elephant_pressure, elephant_path = max(
        dfs(0, valves_to_open - set(my_part), 26, "AA"), key=itemgetter(0)
    )
    if my_pressure + elephant_pressure > s2:
        s2 = my_pressure + elephant_pressure
        my_best_path = my_path
        elephant_best_path = elephant_path

print(s2)
print(my_best_path)
print(elephant_best_path)
