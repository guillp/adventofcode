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
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c in ".S"
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
        print(
            "".join(
                "O" if (x, y) in pos else "." if (x, y) in grid else "#"
                for x in range(W)
            )
        )


def part2(content: str, steps: int = 26501365) -> int:
    GRID, H, W, X, Y = parse(content)
    # those properties are noticable in the input
    assert H == W == 131  # input is square
    assert X == Y == (H - 1) / 2  # start is at the center
    assert (
        65 + 202300 * 131 == 26501365
    )  # well reach the border of a grid on each direction

    # let's expand 2 grids in each direction, this will form a tile
    tiles = {(0, 0): {(X, Y)}}
    for i in range(65 + 131 * 2):
        next_tiles = {}
        for (tx, ty), tile in tiles.items():
            for x, y in tile:
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    dgx, rx = divmod(nx, W)
                    dgy, ry = divmod(ny, H)
                    if (rx, ry) in GRID:
                        tile_pos = (tx + dgx, ty + dgy)
                        next_tiles.setdefault(tile_pos, set())
                        next_tiles[tile_pos].add((rx, ry))

        tiles = next_tiles

    # notice some patterns
    assert (
        len(tiles[0, 1]) == len(tiles[1, 0]) == len(tiles[-1, 0]) == len(tiles[0, -1])
    )  # those are fully filled
    assert len(tiles[-1, 2]) == len(tiles[-2, 1])  # upper left corners
    assert len(tiles[-1, -2]) == len(tiles[-2, -1])  # lower left corners
    assert len(tiles[1, 2]) == len(tiles[2, 1])  # upper right corners
    assert len(tiles[1, -2]) == len(tiles[2, -1])  # lower

    N = 202300
    # number of plots in the starting cell (even)
    even = len(tiles[0, 0])
    # number of plots in any cell adjacent to the starting cell (odd)
    odd = len(tiles[1, 0])

    # number of plots in the 4 unreachable corners of half of the border cells.
    # since N is even, those border cells are also even.
    # those corners must be removed from the total since they are not reachable
    even_corners = len(tiles[0, 0] - tiles[0, 2]) + len(tiles[0, 0] - tiles[0, -2])

    # number of reachable plots in the 4 corners in the other half of the border cells
    odd_corners = (
        len(tiles[-1, 2]) + len(tiles[-1, -2]) + len(tiles[1, 2]) + len(tiles[1, -2])
    )

    return (
        (N + 1) ** 2 * even  # there are that many even tiles in the diamond
        + N**2 * odd  # that many odd tiles
        - (N + 1) * even_corners  # that many even corners to remove
        + N * odd_corners  # and that many odd corners to add
    )


assert part1(test_content, steps=6) == 16
print(part1(content))

print(part2(content))
