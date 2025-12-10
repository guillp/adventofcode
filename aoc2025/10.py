import re
from itertools import count


def parse_input(machine: str) -> tuple[tuple[bool, ...], tuple[tuple[int, ...]], tuple[int, ...]]:
    indicators_str, *wires_str, joltage_str = re.findall(r"[\.#]+|(?:\d+,?)+", machine)
    indicators = tuple(c == "#" for c in indicators_str)
    wires = tuple(tuple(int(n) for n in wiring_str.split(",")) for wiring_str in wires_str)
    joltages = tuple(int(n) for n in joltage_str.split(","))
    return indicators, wires, joltages


def step(wires, pool):
    for path, state in pool.items():
        for i, button in enumerate(wires):
            if path and i == path[-1]:
                continue
            new_state = tuple(not c if i in button else c for i, c in enumerate(state))
            yield (*path, i), new_state


def bfs(target, wires):
    pool = {(): (False,) * len(target)}
    for n in count(1):
        new_pool = {}
        for path, state in step(wires, pool):
            if state == target:
                return n
            new_pool[path] = state
        pool = new_pool


def solve(content: str):
    part1 = 0
    for machine in content.splitlines():
        target, wires, joltages = parse_input(machine)
        part1 += bfs(target, wires)

    return part1


test_content = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

assert solve(test_content) == 7


with open("10.txt") as f:
    content = f.read()

print(solve(content))
