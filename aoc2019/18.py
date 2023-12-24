from functools import cache
from heapq import heappush, heappop


def part1(content: str) -> int:
    lines = content.splitlines()

    grid = {
        complex(x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c != "#"
    }

    start_pos = next(pos for pos, c in grid.items() if c == "@")

    # turn the labyrinth into a graph using a quick DFS
    G = {"@": {}}
    pool = [(0, "@", "", (start_pos,))]
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
                # this is required because
                if G[key_or_gate].get(start_symbol, (None, float("inf")))[1] > len(
                    path
                ):
                    G[key_or_gate][start_symbol] = G[start_symbol][
                        key_or_gate
                    ] = required_gates, len(path)

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
    def solve(current_key: str, missing_keys: frozenset) -> int:
        if not missing_keys:
            return 0
        best = float("inf")
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


with open("18.txt") as f:
    content = f.read()

print(part1(content))


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
