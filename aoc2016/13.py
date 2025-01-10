def is_wall(x: int, y: int, n: int) -> bool:
    return f"{x * x + 3 * x + 2 * x * y + y + y * y + n:b}".count("1") % 2 == 1


assert not is_wall(0, 0, 10)
assert is_wall(1, 0, 10)
assert is_wall(1, 3, 10)
assert is_wall(9, 6, 10)


def part1(dx: int, dy: int, n: int) -> int:
    pool: list[tuple[tuple[int, int], ...]] = [((1, 1),)]
    best = (dx + 1) * (dy + 1)
    while pool:
        pool.sort(key=len, reverse=True)
        path = pool.pop()
        if len(path) - 1 >= best:
            continue

        x, y = path[-1]

        for nx, ny in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or (nx, ny) in path or is_wall(nx, ny, n):
                continue

            if nx == dx and ny == dy:
                best = len(path)
            else:
                pool.append((*path, (nx, ny)))

    return best


def part2(n: int) -> int:
    reachable = {(1, 1)}

    pool: list[tuple[tuple[int, int], ...]] = [((1, 1),)]
    while pool:
        path = pool.pop()

        x, y = path[-1]

        for nx, ny in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or (nx, ny) in path or is_wall(nx, ny, n):
                continue

            reachable.add((nx, ny))
            if len(path) < 50:
                pool.append((*path, (nx, ny)))

    return len(reachable)


content = 1352

assert part1(7, 4, 10) == 11
print(part1(31, 39, content))
print(part2(content))
