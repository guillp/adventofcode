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
def arrange(positions: str, groups: tuple[int]) -> int:
    while positions and positions[0] == ".":  # remove unwanted leading dots
        positions = positions[1:]

    while positions and positions.endswith(".."):  # remove trailing dots
        positions = positions[:-1]

    if positions and positions[-1] != ".":
        positions += "."  # add an extra dot at the end to simplify our logic

    if not groups and "#" not in positions:
        return 1
    if sum(groups) > len(positions) or not groups and "#" in positions:
        return 0  # fail fast on impossible cases

    s = 0
    if (
        "." not in positions[: groups[0]]  # the next group fits
        and positions[groups[0]] in ".?"
    ):  # there is a separator after the group
        s += arrange(positions[groups[0] + 1 :], groups[1:])

    if positions[0] in ".?":  # try the same alg without the leading . or ?
        s += arrange(positions[1:], groups)

    return s


assert arrange(".??..??...?##.", (1, 1, 3)) == 4
assert arrange("?#?#?#?#?#?#?#?", (1, 3, 1, 6)) == 1
assert arrange("????.#...#...", (4, 1, 1)) == 1
assert arrange("????.######..#####.", (1, 6, 5)) == 4
assert arrange("?###????????", (3, 2, 1)) == 10


def part1(content: str) -> int:
    arrangements = 0
    for line in content.splitlines():
        positions, groups = line.split()
        arrangements += arrange(positions, tuple(int(x) for x in groups.split(",")))
    return arrangements


def part2(content: str) -> int:
    arrangements = 0
    for line in content.splitlines():
        positions, groups = line.split()
        positions = "?".join(positions for _ in range(5))
        arrangements += arrange(positions, tuple(int(x) for x in groups.split(",")) * 5)
    return arrangements


test_content = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

assert part1(test_content) == 21
assert part2(test_content) == 525152

print(part1(content))
print(part2(content))
