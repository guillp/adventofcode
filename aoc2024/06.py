from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    lines = content.strip().splitlines()
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    init_guard = guard = next(pos for pos, c in grid.items() if c == "^")
    grid[guard] = "."
    direction = -1j
    visited = {guard}

    while guard in grid:
        next_pos = guard + direction
        if next_pos not in grid:
            yield len(visited)
            break
        if grid[next_pos] == "#":
            direction *= 1j
        else:
            guard = next_pos
            visited.add(next_pos)

    possible_locations = set()
    for location in visited.copy():
        new_grid = grid.copy()
        new_grid[location] = "#"
        guard = init_guard
        direction = -1j
        visited = {(guard, direction)}
        while guard in grid:
            next_pos = guard + direction
            if (next_pos, direction) in visited:
                possible_locations.add(location)
                break
            if next_pos not in new_grid:
                break
            if new_grid[next_pos] == "#":
                direction *= 1j
            else:
                guard = next_pos
                visited.add((next_pos, direction))

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
