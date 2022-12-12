with open('18.txt', "rt") as finput:
    content = finput.read()

grid = {
    complex(x, y): c == '#'
    for y, line in enumerate(content.splitlines())
    for x, c in enumerate(line)
}

SIZE = 100


def step(grid: dict[complex, bool]):
    new_grid = {}
    for x in range(SIZE):
        for y in range(SIZE):
            coord = complex(x, y)
            nb_neighbours = sum(
                grid.get(coord + X + Y, False)
                for X in (-1, 0, 1)
                for Y in (-1j, 0, 1j)
                if not X == Y == 0
            )
            if grid[coord]:
                new_grid[coord] = nb_neighbours in (2, 3)
            else:
                new_grid[coord] = nb_neighbours == 3

    return new_grid


for i in range(100):
    # print(i)
    # for y in range(SIZE):
    # print("".join("#" if grid[complex(x, y)] else '.' for x in range(SIZE)))
    grid = step(grid)

print(sum(grid.values()))

grid2 = {
    complex(x, y): c == '#'
    for y, line in enumerate(content.splitlines())
    for x, c in enumerate(line)
}
for x in (0, 99):
    for y in (0, 99):
        grid2[complex(x, y)] = True


def step2(grid: dict[complex, bool]):
    new_grid = {}
    for x in range(SIZE):
        for y in range(SIZE):
            coord = complex(x, y)
            if coord in (0, 0 + 99j, 99 + 99j, 99):
                new_grid[coord] = True
            else:
                nb_neighbours = sum(
                    grid.get(coord + X + Y, False)
                    for X in (-1, 0, 1)
                    for Y in (-1j, 0, 1j)
                    if not X == Y == 0
                )
                if grid[coord]:
                    new_grid[coord] = nb_neighbours in (2, 3)
                else:
                    new_grid[coord] = nb_neighbours == 3

    return new_grid


for i in range(100):
    print(i)
    for y in range(SIZE):
        print("".join("#" if grid2[complex(x, y)] else '.' for x in range(SIZE)))
    grid2 = step2(grid2)

print(sum(grid2.values()))
