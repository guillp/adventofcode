import re
from heapq import heappop, heappush


def operators(result: int, *numbers: int, part2: bool = False) -> bool:
    pool = [numbers]
    while pool:
        left, right, *others = heappop(pool)
        candidates = {left + right, left * right}
        if part2:
            candidates.add(int(f"{left}{right}"))
        for candidate in candidates:
            if candidate == result and not others:
                return True
            if candidate <= result and others:
                heappush(pool, (candidate, *others))

    return False


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for line in content.strip().splitlines():
        result, *numbers = (int(x) for x in re.findall(r"\d+", line))
        if operators(result, *numbers):
            part1 += result
        elif operators(result, *numbers, part2=True):
            part2 += result

    return part1, part1 + part2


test_content = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

assert tuple(solve(test_content)) == (3749, 11387)

with open("07.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
