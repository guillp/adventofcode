from functools import cache


@cache
def arrange(design: bytes, towels: tuple[bytes]) -> int:
    if design == b"":
        return 1
    return sum(arrange(design[len(towel) :], towels) for towel in towels if design.startswith(towel))


def solve(content: str) -> tuple[int, int]:
    towels_part, designs_part = content.strip().split("\n\n")
    towels = tuple(towels_part.encode().split(b", "))

    part1 = part2 = 0
    for design in designs_part.encode().splitlines():
        possibilities = arrange(design, towels)
        part1 += bool(possibilities)
        part2 += possibilities

    return part1, part2


test_content = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

assert tuple(solve(test_content)) == (6, 16)

with open("19.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
