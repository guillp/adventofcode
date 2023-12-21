test_content = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

with open("21.txt") as f:
    content = f.read()


def parse(content: str) -> tuple[frozenset(tuple[int, int]), int, int, tuple[int, int]]:
    lines = content.splitlines()
    H = len(lines)
    W = len(lines[0])
    grid = frozenset(
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c in ".S"
    )
    start_pos = next(pos for pos, c in grid.items() if c == "S")
    grid[start_pos] = "."
    return grid, H, W, start_pos


def part1(content: str, steps: int = 64) -> int:
    grid, H, W, start_pos = parse(content)
    cells = {start_pos}
    for i in range(steps):
        next_cells = set()
        for x, y in cells:
            for next_cell in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if next_cell in grid:
                    next_cells.add(next_cell)
        cells = next_cells

    return len(cells)


def part2(content: str, steps: int = 26501365) -> int:
    grid, H, W, start_pos = parse(content)
    cells = {(0, 0, start_pos)}
    for i in range(steps):
        next_cells = set()
        for x, y in cells:
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx % H, ny % W) in grid:
                    next_cells.add((nx, ny))
        cells = next_cells

    return len(cells)


assert part1(test_content, steps=6) == 16
print(part1(content))

assert part2(test_content, steps=6) == 16
print(6)
assert part2(test_content, steps=10) == 50
print(10)
assert part2(test_content, steps=50) == 1594
print(50)
assert part2(test_content, steps=100) == 6536
print(100)
assert part2(test_content, steps=500) == 167004
print(500)
assert part2(test_content, steps=5000) == 16733044
print(5000)
print(part2(content))
