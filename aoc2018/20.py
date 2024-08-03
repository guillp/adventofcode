from collections import defaultdict

DIRECTIONS = {"N": -1j, "E": 1, "S": 1j, "W": -1}


def solve(content: str) -> tuple[int, int]:
    pos = 0j
    G: dict[complex, set[complex]] = defaultdict(set)
    levels = {}
    level = 0
    for c in content:
        match c:
            case "^" if G:
                assert False, "Unexpected ^"
            case "(":
                level += 1
                levels[level] = pos
            case ")":
                pos = levels[level]
                level -= 1
            case "|":
                pos = levels[level]
            case "$" if level != 0:
                assert False, "Unexpected $"
            case _ if c in DIRECTIONS:
                d = DIRECTIONS[c]
                G[pos].add(pos + d)
                G[pos + d].add(pos)
                pos += d

    pool: list[tuple[int, tuple[complex, ...]]] = [(0, (0j,))]
    longest = 0
    more_than_1000 = set()
    while pool:
        dist, path = pool.pop()
        longest = max(longest, dist)
        pos = path[-1]
        if dist >= 1000:
            more_than_1000.add(pos)
        for next_pos in G[pos]:
            if next_pos in path:
                continue  # don't walk twice in the same room
            pool.append((dist + 1, path + (next_pos,)))

    return longest, len(more_than_1000)


assert solve("^WNE$") == (3, 0)
assert solve("^ENWWW(NEEE|SSE(EE|N))$") == (10, 0)
assert solve("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$") == (18, 0)
assert solve("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$") == (23, 0)
assert solve("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$") == (31, 0)

with open("20.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
