def part1(content: str) -> int:
    jumps = [int(x) for x in content.splitlines()]
    i = step = 0
    while 0 <= step < len(jumps):
        s = jumps[step]
        jumps[step] += 1
        step += s
        i += 1
    return i


def part2(content: str) -> int:
    jumps = [int(x) for x in content.splitlines()]
    i = step = 0
    while 0 <= step < len(jumps):
        s = jumps[step]
        if s >= 3:
            jumps[step] -= 1
        else:
            jumps[step] += 1
        step += s
        i += 1
    return i


test_content = """\
0
3
0
1
-3
"""


assert part1(test_content) == 5
assert part2(test_content) == 10


with open("05.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
