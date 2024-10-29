import re
from collections import defaultdict


def solve(content: str, *, part2: bool = False) -> int:
    counter = defaultdict[tuple[int, int], int](int)

    for line in content.strip().splitlines():
        x1, y1, x2, y2 = (int(x) for x in re.findall(r"\d+", line))
        if (x2, y2) < (x1, y1):
            x1, y1, x2, y2 = x2, y2, x1, y1
        if not part2 and x1 != x2 and y1 != y2:
            continue
        xd = 1 if x2 > x1 else 0
        yd = 1 if y2 > y1 else -1 if y2 < y1 else 0
        for i in range(max(x2 - x1 + 1, abs(y2 - y1) + 1)):
            counter[x1 + i * xd, y1 + i * yd] += 1

    return sum(count > 1 for point, count in counter.items())


test_content = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
assert solve(test_content) == 5
assert solve(test_content, part2=True) == 12

with open("05.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
