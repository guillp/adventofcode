from itertools import combinations

test_content = """\
5 1 9 5
7 5 3
2 4 6 8"""

test_content2 = """\
5 9 2 8
9 4 7 3
3 8 6 5
"""

def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for row in content.splitlines():
        ints = tuple(int(x) for x in row.split())
        part1 += max(ints) - min(ints)
        for a, b in combinations(sorted(ints, reverse=True), 2):
            if a % b == 0:
                part2 += a // b
    return part1, part2


assert solve(test_content)[0] == 18
assert solve(test_content2)[1] == 9

with open("02.txt") as f:
    content = f.read()

print(*solve(content), sep="\n")
