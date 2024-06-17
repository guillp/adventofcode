def solve(serial_number: int, part2: bool = False) -> str:
    min_square_size = 1 if part2 else 3
    max_square_size = 300 if part2 else 3
    grid_size = 300

    grid = {
        (x, y): (((x + 10) * y + serial_number) * (x + 10) // 100) % 10 - 5
        for x in range(1, grid_size + 1)
        for y in range(1, grid_size + 1)
    }

    max_power = -5 * 9
    max_x = max_y = -1
    max_size = -1
    for square_size in range(min_square_size, max_square_size + 1):
        for x in range(1, grid_size - square_size):
            for y in range(1, grid_size - square_size):
                power = sum(grid[x + dx, y + dy] for dx in range(square_size) for dy in range(square_size))
                if power > max_power:
                    max_power, max_x, max_y, max_size = power, x, y, square_size

    return f"{max_x},{max_y},{max_size}" if part2 else f"{max_x},{max_y}"


SERIAL = 9445
print(solve(SERIAL))
print(solve(SERIAL, part2=True))
