from itertools import product


def solve(content: str) -> tuple[int, int]:
    lines = content.strip().splitlines()
    height = len(lines)
    width = len(lines[0])
    assert height == width
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    part1 = part2 = 0
    for x, y in product(range(height), repeat=2):
        pos = complex(x, y)
        for direction in (-1j, 1 - 1j, 1, 1 + 1j, 1j, -1 + 1j, -1, -1 - 1j):
            if "".join(grid.get(pos + i * direction, ".") for i in range(4)) == "XMAS":
                part1 += 1

        if grid.get(pos) == "A" and {
            grid.get(pos - 1 - 1j),
            grid.get(pos + 1 + 1j),
        } == {
            grid.get(pos + 1 - 1j),
            grid.get(pos - 1 + 1j),
        } == {
            "M",
            "S",
        }:
            part2 += 1
    return part1, part2


test_content = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
assert solve(test_content) == (18, 9)

with open("04.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
