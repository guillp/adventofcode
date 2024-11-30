def solve(content: str) -> int:
    lines = content.strip().splitlines()
    height, width = len(lines), len(lines[0])
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "."}

    for step in range(1, 10_000):
        new_grid = grid.copy()

        for (x, y), c in grid.items():
            if c == ">":
                next_pos = (x + 1) % width, y
                if next_pos not in grid:
                    new_grid[next_pos] = ">"
                    del new_grid[x, y]

        grid_after_east = new_grid.copy()
        for (x, y), c in grid.items():
            if c == "v":
                next_pos = x, (y + 1) % height
                if next_pos not in grid_after_east:
                    new_grid[next_pos] = "v"
                    del new_grid[x, y]

        if grid == new_grid:
            return step
        grid = new_grid

    assert False, "Solution not found!"


test_content = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
assert solve(test_content) == 58

with open("25.txt") as f:
    content = f.read()

print(solve(content))
