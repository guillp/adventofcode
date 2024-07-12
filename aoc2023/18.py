def shoelace_area(*points: tuple[int, int]) -> float:
    x, y = zip(*points, strict=False)
    return (  # type: ignore[no-any-return]
        abs(
            sum(i * j for i, j in zip(x, y[1:] + y[:1], strict=False))
            - sum(i * j for i, j in zip(x[1:] + x[:1], y, strict=False))
        )
        / 2
    )


def part1_parser(line: str) -> tuple[int, int]:
    direction, dststr, _ = line.split()
    dst = int(dststr)
    dx, dy = {"U": (0, 1), "D": (0, -1), "L": (1, 0), "R": (-1, 0)}[direction]
    return dx * dst, dy * dst


def part2_parser(line: str) -> tuple[int, int]:
    _, _, color = line.split()
    dst = int(color[2:-2], 16)
    dx, dy = {"3": (0, 1), "1": (0, -1), "2": (1, 0), "0": (-1, 0)}[color[-2]]
    return dx * dst, dy * dst


def solve(content: str, part2: bool = False) -> int:
    x = y = 0
    points = []
    border = 0
    for line in content.splitlines():
        if not part2:
            dx, dy = part1_parser(line)
        else:
            dx, dy = part2_parser(line)

        x += dx
        y += dy
        border += abs(dx + dy)
        points.append((x, y))

    assert x == y == 0
    return int(shoelace_area(*points) + border / 2) + 1


test_content = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

assert solve(test_content) == 62
assert solve(test_content, part2=True) == 952408144115

with open("18.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
