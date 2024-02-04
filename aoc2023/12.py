from functools import cache

content = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

with open("12.txt") as f:
    content = f.read()


@cache
def solve(positions: str, groups: tuple[int]) -> int:
    while positions and positions[0] == ".":  # remove unwanted leading dots
        positions = positions[1:]

    while positions and positions[-2:] == "..":  # remove trailing dots
        positions = positions[:-1]

    if positions and positions[-1] != ".":
        positions += "."  # add an extra dot at the end to simplify our logic

    if not groups and "#" not in positions:
        return 1
    if sum(groups) > len(positions) or not groups and "#" in positions:
        return 0  # fail fast on impossible cases

    s = 0
    if "." not in positions[: groups[0]]:  # the next group fits
        if positions[groups[0]] in ".?":  # there is a separator after the group
            s += solve(positions[groups[0] + 1 :], groups[1:])

    if positions[0] in ".?":  # try the same alg without the leading . or ?
        s += solve(positions[1:], groups)

    return s


assert solve(".??..??...?##.", (1, 1, 3)) == 4
assert solve("?#?#?#?#?#?#?#?", (1, 3, 1, 6)) == 1
assert solve("????.#...#...", (4, 1, 1)) == 1
assert solve("????.######..#####.", (1, 6, 5)) == 4
assert solve("?###????????", (3, 2, 1)) == 10

part1 = 0
for line in content.splitlines():
    positions, groups = line.split()
    part1 += solve(positions, tuple(int(x) for x in groups.split(",")))
print(part1)

part2 = 0
for line in content.splitlines():
    positions, groups = line.split()
    positions = "?".join(positions for _ in range(5))
    part2 += solve(positions, tuple(int(x) for x in groups.split(",")) * 5)
print(part2)
