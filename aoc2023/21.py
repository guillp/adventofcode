from collections.abc import Iterator


def parse(content: str) -> tuple[frozenset[tuple[int, int]], int, int, int, int]:
    lines = content.strip().splitlines()
    H = len(lines)
    W = len(lines[0])
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c in ".S"}
    x, y = next(pos for pos, c in grid.items() if c == "S")
    return frozenset(grid), H, W, x, y


def solve(content: str, part1_steps: int = 64, part2_steps: int = 26501365) -> Iterator[int]:
    grid, height, width, start_x, start_y = parse(content)
    cells = {(start_x, start_y)}
    for _ in range(part1_steps):
        next_cells = set()
        for x, y in cells:
            for next_cell in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if next_cell in grid:
                    next_cells.add(next_cell)
        cells = next_cells

    yield len(cells)

    assert height == width  # input is square
    assert start_x == start_y == (height - 1) // 2  # start is at the center
    div, mod = divmod(part2_steps, height)
    assert mod == height // 2

    # let's expand 2 grids in each direction, this will form a tile
    tiles = {(0, 0): {(start_x, start_y)}}
    for _ in range(mod + height * 2):
        next_tiles: dict[tuple[int, int], set[tuple[int, int]]] = {}
        for (tx, ty), tile in tiles.items():
            for start_x, start_y in tile:
                for nx, ny in (
                    (start_x + 1, start_y),
                    (start_x - 1, start_y),
                    (start_x, start_y + 1),
                    (start_x, start_y - 1),
                ):
                    dgx, rx = divmod(nx, width)
                    dgy, ry = divmod(ny, height)
                    if (rx, ry) in grid:
                        tile_pos = (tx + dgx, ty + dgy)
                        next_tiles.setdefault(tile_pos, set())
                        next_tiles[tile_pos].add((rx, ry))

        tiles = next_tiles

    # notice some patterns
    assert len(tiles[0, 1]) == len(tiles[1, 0]) == len(tiles[-1, 0]) == len(tiles[0, -1])  # those are fully filled
    assert len(tiles[-1, 2]) == len(tiles[-2, 1])  # upper left corners
    assert len(tiles[-1, -2]) == len(tiles[-2, -1])  # lower left corners
    assert len(tiles[1, 2]) == len(tiles[2, 1])  # upper right corners
    assert len(tiles[1, -2]) == len(tiles[2, -1])  # lower

    # number of plots in the starting cell (even)
    even = len(tiles[0, 0])
    # number of plots in any cell adjacent to the starting cell (odd)
    odd = len(tiles[1, 0])

    # number of plots in the 4 unreachable corners of half of the border cells.
    # since N is even, those border cells are also even.
    # those corners must be removed from the total since they are not reachable
    even_corners = len(tiles[0, 0] - tiles[0, 2]) + len(tiles[0, 0] - tiles[0, -2])

    # number of reachable plots in the 4 corners in the other half of the border cells
    odd_corners = len(tiles[-1, 2]) + len(tiles[-1, -2]) + len(tiles[1, 2]) + len(tiles[1, -2])

    yield (
        (div + 1) ** 2 * even  # there are that many even tiles in the diamond
        + div**2 * odd  # that many odd tiles
        - (div + 1) * even_corners  # that many even corners to remove
        + div * odd_corners  # and that many odd corners to add
    )


def print_grid(height: int, width: int, grid: set[tuple[int, int]], pos: set[tuple[int, int]]) -> None:
    for y in range(height):
        print("".join("O" if (x, y) in pos else "." if (x, y) in grid else "#" for x in range(width)))


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

assert next(solve(test_content, part1_steps=6)) == 16

with open("21.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
