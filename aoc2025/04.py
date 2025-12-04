def solve(content: str) -> tuple[int, int]:
    grid = {complex(x, y) for y, line in enumerate(content.splitlines()) for x, c in enumerate(line) if c == "@"}

    part1 = part2 = 0
    while True:
        new_grid = {
            p
            for p in grid
            if sum(p + x + y in grid for x in (-1, 0, 1) for y in (-1j, 0, 1j) if not (x == y == 0)) >= 4
        }
        if new_grid == grid:
            break
        if part1 == 0:
            part1 = len(grid) - len(new_grid)
        part2 += len(grid) - len(new_grid)
        grid = new_grid

    return part1, part2


test_content = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

assert solve(test_content) == (13, 43)

with open("04.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
