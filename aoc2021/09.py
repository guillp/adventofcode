from collections.abc import Iterator


def solve(content: str) -> tuple[int, int]:
    grid = {complex(x, y): int(c) for y, line in enumerate(content.strip().splitlines()) for x, c in enumerate(line)}

    def iter_low_points() -> Iterator[tuple[complex, int]]:
        for point, height in grid.items():
            if all(grid.get(point + d, 10) > height for d in (1, -1, 1j, -1j)):
                yield point, height

    part1 = 0
    basins = []
    for low_point, height in iter_low_points():
        part1 += height + 1
        to_visit = {low_point}
        visited = set()
        while to_visit:
            point = to_visit.pop()
            visited.add(point)
            for nb in (point + 1, point - 1, point + 1j, point - 1j):
                if nb in visited or grid.get(nb, 9) == 9:
                    continue
                to_visit.add(nb)
        basins.append(len(visited))

    part2 = 1
    for basin in sorted(basins)[-3:]:
        part2 *= basin

    return part1, part2


assert solve("""\
2199943210
3987894921
9856789892
8767896789
9899965678
""") == (15, 1134)

with open("09.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
