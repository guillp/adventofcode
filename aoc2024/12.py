from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    lines = content.strip().splitlines()
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}

    regions = {}
    visited = set()
    for pos, label in grid.items():
        if pos in visited:
            continue
        region = {pos}
        perimeter = 0
        to_visit = {pos}
        while to_visit:
            x, y = to_visit.pop()
            for next_pos in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                next_label = grid.get(next_pos)
                if next_label == label:
                    if next_pos not in region:
                        region.add(next_pos)
                        to_visit.add(next_pos)
                elif next_label != label:
                    perimeter += 1
        visited |= region
        regions[frozenset(region)] = perimeter

    yield sum(len(region) * perimeter for region, perimeter in regions.items())


test_content = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

assert tuple(solve(test_content)) == (1930, 1206)

with open("12.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
