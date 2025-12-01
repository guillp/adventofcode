from collections.abc import Iterable
from functools import cache
from itertools import pairwise

numeric_keypad = {
    "7": 0,
    "8": 1,
    "9": 2,
    "4": 1j,
    "5": 1 + 1j,
    "6": 2 + 1j,
    "1": 2j,
    "2": 1 + 2j,
    "3": 2 + 2j,
    "0": 1 + 3j,
    "A": 2 + 3j,
}

direction_keypad = {
    "^": 1,
    "A": 2,
    "<": 1j,
    "v": 1 + 1j,
    ">": 2 + 1j,
}


def best_path(
    left: str,
    right: str,
    keypad: dict[str, complex],
) -> str:
    current_pos = keypad[left]
    target_pos = keypad[right]

    def greedy(pos: complex, *keys: str) -> Iterable[str]:
        if pos == target_pos:
            yield "".join((*keys, "A"))
        if pos.real > target_pos.real and pos - 1 in keypad.values():
            yield from greedy(pos - 1, *keys, "<")
        if pos.imag > target_pos.imag and pos - 1j in keypad.values():
            yield from greedy(pos - 1j, *keys, "^")
        if pos.imag < target_pos.imag and pos + 1j in keypad.values():
            yield from greedy(pos + 1j, *keys, "v")
        if pos.real < target_pos.real and pos + 1 in keypad.values():
            yield from greedy(pos + 1, *keys, ">")

    return min(
        greedy(current_pos),
        key=lambda path: (
            len(path),  # favor the shortest path
            sum(a != b for a, b in pairwise(path)),  # with the least number of key changes
        ),
    )


@cache
def key_presses(sequence: str, n: int, level: int = 0) -> int:
    if level == n:
        return len(sequence)
    return sum(
        key_presses(best_path(left, right, numeric_keypad if level == 0 else direction_keypad), n, level + 1)
        for left, right in pairwise("A" + sequence)
    )


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for code in content.strip().splitlines():
        part1 += key_presses(code, 3) * int(code[:-1])
        part2 += key_presses(code, 26) * int(code[:-1])
    return part1, part2


test_content = """\
029A
980A
179A
456A
379A
"""

assert solve(test_content) == (126384, 154115708116294)


with open("21.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
