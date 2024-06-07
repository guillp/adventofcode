SIZE = 100


def part1(content: str) -> int:
    grid = {complex(x, y): c == "#" for y, line in enumerate(content.splitlines()) for x, c in enumerate(line)}

    def step(grid: dict[complex, bool]) -> dict[complex, bool]:
        new_grid = {}
        for x in range(SIZE):
            for y in range(SIZE):
                coord = complex(x, y)
                nb_neighbours = sum(
                    grid.get(coord + X + Y, False) for X in (-1, 0, 1) for Y in (-1j, 0, 1j) if not X == Y == 0
                )
                if grid[coord]:
                    new_grid[coord] = nb_neighbours in (2, 3)
                else:
                    new_grid[coord] = nb_neighbours == 3

        return new_grid

    for _ in range(100):
        grid = step(grid)

    return sum(grid.values())


def part2(content: str) -> int:
    grid = {complex(x, y): c == "#" for y, line in enumerate(content.splitlines()) for x, c in enumerate(line)}

    for x in (0, 99):
        for y in (0, 99):
            grid[complex(x, y)] = True

    def step(grid: dict[complex, bool]) -> dict[complex, bool]:
        new_grid = {}
        for x in range(SIZE):
            for y in range(SIZE):
                coord = complex(x, y)
                if coord in (0, 0 + 99j, 99 + 99j, 99):
                    new_grid[coord] = True
                else:
                    nb_neighbours = sum(
                        grid.get(coord + X + Y, False) for X in (-1, 0, 1) for Y in (-1j, 0, 1j) if not X == Y == 0
                    )
                    if grid[coord]:
                        new_grid[coord] = nb_neighbours in (2, 3)
                    else:
                        new_grid[coord] = nb_neighbours == 3

        return new_grid

    for _ in range(100):
        grid = step(grid)

    return sum(grid.values())


with open("18.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
