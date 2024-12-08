from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    lines = content.strip().splitlines()
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    init_guard = guard = next(pos for pos, c in grid.items() if c == "^")
    grid[guard] = "."
    direction = -1j

    visited = set()
    while guard in grid:
        visited.add(guard)
        if grid.get(guard + direction) == "#":
            direction *= 1j
        guard += direction

    yield len(visited)

    possible_locations = set()
    for location in visited.copy():
        new_grid = grid | {location: "#"}
        guard = init_guard
        direction = -1j
        visited2 = set()
        while guard in new_grid:
            if (guard, direction) in visited2:
                possible_locations.add(location)
                break
            visited2.add((guard, direction))
            if new_grid.get(guard + direction) == "#":
                direction *= 1j
            guard += direction

    yield len(possible_locations)


test_content = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

assert tuple(solve(test_content)) == (41, 6)

with open("06.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
