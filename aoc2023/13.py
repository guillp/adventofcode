from collections.abc import Iterator


def find_mirror(pattern: str, *, part2: bool = False) -> int:
    lines = pattern.splitlines()
    H = len(lines)
    W = len(lines[0])

    # vertical
    for x in range(1, W):
        errors = 0
        for y in range(H):
            for i in range(min(x, W - x)):
                left = x - 1 - i
                right = x + i
                if lines[y][left] != lines[y][right]:
                    errors += 1

        if not part2 and errors == 0:
            return x
        if part2 and errors == 1:
            return x

    # horizontal
    for y in range(1, H):
        errors = 0
        for x in range(W):
            for i in range(min(y, H - y)):
                up = y - 1 - i
                down = y + i
                if lines[up][x] != lines[down][x]:
                    errors += 1

        if not part2 and errors == 0:
            return y * 100
        if part2 and errors == 1:
            return y * 100

    return 0


def solve(content: str) -> Iterator[int]:
    patterns = content.split("\n\n")

    part1 = 0
    for pattern in patterns:
        part1 += find_mirror(pattern)
    yield part1

    part2 = 0
    for pattern in patterns:
        part2 += find_mirror(pattern, part2=True)
    yield part2


test_content = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

assert tuple(solve(test_content)) == (405, 400)

with open("13.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
