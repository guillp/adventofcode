from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    lines = content.strip().splitlines()
    H, W = len(lines), len(lines[0])
    trees = {(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"}
    part1 = sum((y * 3 % W, y) in trees for y in range(H))
    yield part1
    for slope_x, slope_y in ((1, 1), (5, 1), (7, 1), (1, 2)):
        part1 *= sum(((y * slope_x // slope_y) % W, y) in trees for y in range(0, H, slope_y))
    yield part1


assert tuple(
    solve("""\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""),
) == (7, 336)

with open("03.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
