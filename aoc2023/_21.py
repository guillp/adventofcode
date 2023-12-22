from collections import deque, defaultdict

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
    grid = {
        (x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c in ".S"
    }
    x, y = next(pos for pos, c in grid.items() if c == "S")
    return frozenset(grid), H, W, x, y


def part1(content: str, steps: int = 64) -> int:
    grid, H, W, x, y = parse(content)
    cells = {(x, y)}
    for i in range(steps):
        next_cells = set()
        for x, y in cells:
            for next_cell in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if next_cell in grid:
                    next_cells.add(next_cell)
        cells = next_cells

    return len(cells)

def print_grid(H: int, W: int, grid: set[tuple[int, int]], pos: set[tuple[int, int]]):
    for y in range(H):
        print("".join("O" if (x,y) in pos else "." if (x,y) in grid else "#" for x in range(W)))



def part2(content: str, steps: int = 26501365) -> int:
    grid, H, W, x, y = parse(content)
    assert H == W == 131 # input is square
    assert x == y == (H-1)/2 # start at the center
    assert 65 + 202300 * 131 == 26501365
    cells = {(0, 0): {(x, y)}}

    for i in range(65+131*2):
        next_cells = {}
        for (gx, gy), g in cells.items():
            for x, y in g:
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    dgx, rx = divmod(nx, W)
                    dgy, ry = divmod(ny, H)
                    if (rx, ry) in grid:
                        next_cells.setdefault((gx+dgx, gy+dgy), set())
                        next_cells[gx+dgx, gy+dgy].add((rx,ry))

        cells = next_cells

    assert len(cells[0,1]) == len(cells[1,0]) == len(cells[-1,0]) == len(cells[0,-1]) # those are fully filled
    assert len(cells[-1,2]) == len(cells[-2,1]) # upper left corners
    assert len(cells[-1,-2]) == len(cells[-2,-1]) # lower left corners
    assert len(cells[1,2]) == len(cells[2,1]) # upper right corners
    assert len(cells[1,-2]) == len(cells[2,-1]) # lower

    n = 202300
    return (
            len(cells[0, 2])  # UP
            + len(cells[0, -2])  # DOWN
            + len(cells[-2, 0])  # LEFT
            + len(cells[2, 0])  # RIGHT
            + (
                    len(cells[-1, 2])  # UPPER LEFT ODD CORNER
                    + len(cells[-1, -2])  # LOWER LEFT ODD CORNER
                    + len(cells[1, 2])  # UPPER RIGHT ODD CORNER
                    + len(cells[1, -2])  # LOWER RIGHT ODD CORNER
            ) * n
            + (
                    len(cells[-1, 1])  # UPPER LEFT EVEN CORNER
                    + len(cells[-1, -1])  # LOWER LEFT EVEN CORNER
                    + len(cells[1, 1])  # UPPER RIGHT EVEN CORNER
                    + len(cells[1, -1])  # LOWER RIGHT EVEN CORNER
            ) * (n - 1)
            + len(cells[0, 0]) * (n - 1) ** 2  # EVEN FULL GRID
            + len(cells[1, 0]) * n ** 2  # ODD FULL GRID
    )


assert part1(test_content, steps=6) == 16
print(part1(content))

print(part2(content))
