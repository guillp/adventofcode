from itertools import count


def predict(*numbers: int) -> tuple[int, int]:
    diffs = [tuple(numbers)]
    for i in count(1):
        diff = tuple(b - a for a, b in zip(diffs[i - 1], diffs[i - 1][1:], strict=False))
        if all(d == 0 for d in diff):
            break
        diffs.append(diff)
    after = sum(diff[-1] for diff in diffs)
    before = 0
    for diff in diffs[::-1]:
        before = diff[0] - before
    return before, after


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for line in content.splitlines():
        numbers = tuple(int(x) for x in line.split())
        before, after = predict(*numbers)
        part1 += after
        part2 += before

    return part1, part2


test_content = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

assert solve(test_content) == (114, 2)

with open("09.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
