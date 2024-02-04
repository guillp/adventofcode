from itertools import count

content = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

with open("09.txt") as f:
    content = f.read()


def predict(*numbers: int) -> tuple[int, int]:
    diffs = [tuple(numbers)]
    for i in count(1):
        diff = tuple(b - a for a, b in zip(diffs[i - 1], diffs[i - 1][1:]))
        if all(d == 0 for d in diff):
            break
        diffs.append(diff)
    after = sum(diff[-1] for diff in diffs)
    before = 0
    for diff in diffs[::-1]:
        before = diff[0] - before
    return before, after


part1 = part2 = 0
for line in content.splitlines():
    numbers = tuple(int(x) for x in line.split())
    before, after = predict(*numbers)
    part1 += after
    part2 += before

print(part1)
print(part2)
