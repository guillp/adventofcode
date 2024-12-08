from itertools import combinations, count


def solve(content: str) -> tuple[int, int]:
    grid = {complex(x, y): c for y, line in enumerate(content.strip().splitlines()) for x, c in enumerate(line)}
    antennas_locations = dict[str, set[complex]]()
    for pos, antenna in grid.items():
        if antenna != ".":
            antennas_locations.setdefault(antenna, set()).add(pos)

    part1 = set()
    part2 = set()
    for antenna, locations in antennas_locations.items():
        for left, right in combinations(locations, 2):
            distance = right - left
            if (one := left - distance) in grid:
                part1.add(one)
            if (other := right + distance) in grid:
                part1.add(other)

            for i in count():
                match (one := left - i * distance) in grid, (other := right + i * distance) in grid:
                    case False, False:
                        break
                    case True, True:
                        part2 |= {one, other}
                    case True, False:
                        part2.add(one)
                    case False, True:
                        part2.add(other)

    return len(part1), len(part2)


test_content = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

assert tuple(solve(test_content)) == (14, 34)

with open("08.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
