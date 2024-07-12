import math
import re
from collections.abc import Iterator
from itertools import cycle


def solve(content: str) -> Iterator[int]:
    instructions, _, *nodes = content.splitlines()

    G = {}
    for node in nodes:
        name, left, right = re.findall(r"\w{3}", node)
        G[name] = (left, right)

    pos = "AAA"
    for i, instruction in enumerate(cycle(instructions), start=1):
        pos = G[pos][instruction == "R"]  # indexing on boolean is the same as on 0/1
        if pos == "ZZZ":
            yield i
            break

    positions: dict[str, tuple[str, int | None, int | None]] = {pos: (pos, None, None) for pos in G if pos[-1] == "A"}

    for i, instruction in enumerate(cycle(instructions), start=1):
        for start_pos, (current_pos, ttz, loop) in positions.items():
            if loop is None or ttz is None:
                next_pos = G[current_pos][instruction == "R"]
                if next_pos[-1] == "Z":  # reach destination
                    if ttz is not None:
                        loop = i - ttz
                    else:
                        ttz = i
                positions[start_pos] = (next_pos, ttz, loop)
        if all(None not in v for v in positions.values()):
            break

    for start_pos, (dest_pos, first_seen, loop) in positions.items():
        assert first_seen == loop  # this is verified on I guess all inputs
    yield math.lcm(*tuple(v[1] for v in positions.values()))  # type: ignore[arg-type]


# assert tuple(solve("""\
# RL
#
# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)""")) == (6, 0)

with open("08.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
