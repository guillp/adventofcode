from math import log


def part1(n: int) -> int:
    if n in (1, 2):
        return 1

    if n % 2:
        return 2 * part1((n - 1) // 2) + 1
    return 2 * part1(n // 2) - 1


assert part1(5) == 3
print(part1(3017957))


def part2(n: int) -> int:
    i = int(log(n, 3))
    if 3**i < n <= 2 * 3**i:
        return n - 3**i
    else:
        return 2 * n - 3 ** (i + 1)


assert part2(5) == 2
print(part2(3017957))
