from functools import cache
from heapq import heapify, heappop, heappush


def part1(content: str) -> int:
    lines = content.splitlines()

    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "#"}

    start_pos = next(pos for pos, c in grid.items() if c == "@")

    # turn the labyrinth into a graph using a quick DFS
    G: dict[str, dict[str, tuple[set[str], int]]] = {"@": {}}
    pool: list[tuple[int, str, str, tuple[complex, ...]]] = [(0, "@", "", (start_pos,))]
    while pool:
        steps, start_symbol, traversed, path = pool.pop()
        current_pos = path[-1]
        for d in (1, 1j, -1, -1j):
            next_pos = current_pos + d
            if next_pos not in grid or next_pos in path:
                continue  # don't go off grid or loop
            key_or_gate = grid[next_pos]
            if key_or_gate.islower():  # is a key
                if key_or_gate not in G:
                    pool.append((0, key_or_gate, "", (next_pos,)))
                pool.append(
                    (
                        steps + 1,
                        start_symbol,
                        traversed,
                        path + (next_pos,),
                    )
                )
                G.setdefault(key_or_gate, {})
                required_gates = {gate.lower() for gate in traversed if gate.isupper()}
                # if a distance has been recorded already, make sure we keep the best one
                # this is required because of the multiple possible path around the start position
                if G[key_or_gate].get(start_symbol, (None, float("inf")))[1] > len(path):
                    G[key_or_gate][start_symbol] = G[start_symbol][key_or_gate] = (
                        required_gates,
                        len(path),
                    )

            elif key_or_gate.isupper():  # is a gate
                pool.append(
                    (
                        steps + 1,
                        start_symbol,
                        traversed + key_or_gate,
                        path + (next_pos,),
                    )
                )
            else:  # is just a step
                pool.append((steps + 1, start_symbol, traversed, path + (next_pos,)))

    all_keys = frozenset(c for c in G if c.islower())

    # find the shortest path from @ to all keys
    @cache
    def solve(current_key: str, missing_keys: frozenset[str]) -> int:
        if not missing_keys:
            return 0
        best = len(grid) ** 2
        for key in missing_keys:
            if key in G[current_key]:
                required_gates, cost = G[current_key][key]
                if missing_keys & required_gates:
                    continue
                distance = cost + solve(key, missing_keys - {key})
                if distance < best:
                    best = distance
        return best

    return solve("@", all_keys)


assert (
    part1(
        """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""
    )
    == 86
)

assert (
    part1(
        """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""
    )
    == 132
)

assert (
    part1(
        """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""
    )
    == 136
)

assert (
    part1(
        """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""
    )
    == 81
)


with open("18.txt") as f:
    content = f.read()

print(part1(content))


def part2(content: str) -> int:
    lines = content.splitlines()

    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "#"}

    # adjust the area around the single entrance
    if content.count("@") == 1:
        start_pos = next(pos for pos, c in grid.items() if c == "@")
        assert (
            grid[start_pos - 1]
            == grid[start_pos + 1]
            == grid[start_pos - 1]
            == grid[start_pos - 1j]
            == grid[start_pos + 1j]
            == "."
        )
        del grid[start_pos]
        del grid[start_pos + 1]
        del grid[start_pos - 1]
        del grid[start_pos - 1j]
        del grid[start_pos + 1j]
        grid[start_pos + 1 + 1j] = "@"
        grid[start_pos + 1 - 1j] = "@"
        grid[start_pos - 1 + 1j] = "@"
        grid[start_pos - 1 - 1j] = "@"

    start_positions = [pos for pos, c in grid.items() if c == "@"]

    def dfs(start_pos: complex) -> dict[str, dict[str, tuple[set[str], int]]]:
        G: dict[str, dict[str, tuple[set[str], int]]] = {"@": {}}
        pool: list[tuple[int, str, str, tuple[complex, ...]]] = [(0, "@", "", (start_pos,))]
        while pool:
            steps, start_symbol, traversed, path = pool.pop()
            current_pos = path[-1]
            for d in (1, 1j, -1, -1j):
                next_pos = current_pos + d
                if next_pos not in grid or next_pos in path:
                    continue  # don't go off grid or loop
                key_or_gate = grid[next_pos]
                if key_or_gate.islower():  # is a key
                    if key_or_gate not in G:
                        pool.append((0, key_or_gate, "", (next_pos,)))
                    pool.append(
                        (
                            steps + 1,
                            start_symbol,
                            traversed,
                            path + (next_pos,),
                        )
                    )
                    G.setdefault(key_or_gate, {})
                    required_gates = {gate.lower() for gate in traversed if gate.isupper()}
                    G[key_or_gate][start_symbol] = G[start_symbol][key_or_gate] = (
                        required_gates,
                        len(path),
                    )

                elif key_or_gate.isupper():  # is a gate
                    pool.append(
                        (
                            steps + 1,
                            start_symbol,
                            traversed + key_or_gate,
                            path + (next_pos,),
                        )
                    )
                else:  # is just a step
                    pool.append((steps + 1, start_symbol, traversed, path + (next_pos,)))

        return G

    graphs = [dfs(start_pos) for start_pos in start_positions]
    all_keys = frozenset(c for graph in graphs for c in graph if c.islower())

    sorted_costs = sorted(cost for graph in graphs for d in graph.values() for _, cost in d.values())
    pool: list[tuple[int, int, tuple[int, ...], tuple[str, ...], frozenset[str]]] = [
        (len(all_keys), 0, (0, 0, 0, 0), ("@", "@", "@", "@"), all_keys)
    ]
    heapify(pool)
    best = None
    while pool:
        nb_missing_keys, current_cost, steps, positions, missing_keys = heappop(pool)
        if best is not None and current_cost + sum(sorted_costs[:nb_missing_keys]) >= best:
            continue

        for next_key in missing_keys:
            for i, G in enumerate(graphs):
                current_pos = positions[i]
                if current_pos in G and next_key in G[current_pos]:
                    required_keys, cost = G[current_pos][next_key]
                    if required_keys & missing_keys:
                        continue
                    if len(missing_keys) == 1:
                        if best is None or sum(steps) + cost < best:
                            best = sum(steps) + cost
                    heappush(
                        pool,
                        (
                            nb_missing_keys - 1,
                            current_cost + cost,
                            tuple(s if j != i else s + cost for j, s in enumerate(steps)),
                            tuple(p if j != i else next_key for j, p in enumerate(positions)),
                            missing_keys - {next_key},
                        ),
                    )
    assert best is not None, "Solution not found!"
    return best


assert (
    part2("""\
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""")
    == 8
)

assert (
    part2("""\
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############""")
    == 32
)

print(part2(content))
