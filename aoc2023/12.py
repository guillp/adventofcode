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
    if not positions:
        return 0 if groups else 1
    if not groups:
        return 0 if "#" in positions else 1

    s = 0
    if positions[0] in ".?":  # if the group can't start here
        s += solve(positions[1:], groups)

    if positions[0] in "#?":
        current_len = groups[0]
        if current_len <= len(positions):  # can the current group fit?
            if "." not in positions[:current_len]:
                if "#" not in positions[current_len : current_len + 1]:
                    s += solve(
                        positions[current_len + 1 :],
                        groups[1:],
                    )

    return s


assert solve(".??..??...?##.", (1, 1, 3)) == 4
assert solve("?#?#?#?#?#?#?#?", (1, 3, 1, 6)) == 1
assert solve("????.#...#...", (4, 1, 1)) == 1
assert solve("????.######..#####.", (1, 6, 5)) == 4
assert solve("?###????????", (3, 2, 1)) == 10
s = 0
for line in content.splitlines():
    positions, groups = line.split()
    s += solve(positions, tuple(int(x) for x in groups.split(",")))
print(s)

s = 0
for line in content.splitlines():
    positions, groups = line.split()
    positions = "?".join(positions for _ in range(5))
    s += solve(positions, tuple(int(x) for x in groups.split(",")) * 5)
print(s)
