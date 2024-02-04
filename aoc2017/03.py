content = 289326


def part1(n: int) -> int:
    i = 0
    while (i * 2 + 1) ** 2 < n:
        i += 1

    return i + min(abs(n - x) for x in ((i * 2 + 1) ** 2 - i - i * 2 * j for j in range(4)))


assert part1(12) == 3
assert part1(33) == 4
assert part1(1) == 0
assert part1(1024) == 31
assert part1(23) == 2

print(part1(content))


def part2() -> int:
    class Spiral(dict):
        def __missing__(self, key):
            x, y = key
            v = sum(self.get((x + dx, y + dy), 0) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if not dx == dy == 0)
            self[x, y] = v
            return v

    d = Spiral({(0, 0): 1})

    x = y = i = 0
    while True:
        i += 1
        x += 1
        yield d[x, y]
        for y in range(y - 1, y - i * 2, -1):
            yield d[x, y]
        for x in range(x - 1, x - i * 2 - 1, -1):
            yield d[x, y]
        for y in range(y + 1, y + i * 2 + 1):
            yield d[x, y]
        for x in range(x + 1, x + i * 2 + 1):
            yield d[x, y]


for x in part2():
    if x > content:
        print(x)
        break
