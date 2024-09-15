import re
from collections.abc import Iterator


def neighbors(x: int, y: int, length: int) -> Iterator[tuple[int, int]]:
    yield x - 1, y  # neighbor on the left
    # neighbors above and below
    for d in range(-1, length + 1):
        yield x + d, y - 1
        yield x + d, y + 1
    yield x + length, y  # neighbor on the right


def solve(content: str) -> tuple[int, int]:
    # extract each symbol from input, indexed by position
    symbols = {
        (x, y): c
        for y, line in enumerate(content.splitlines())
        for x, c in enumerate(line)
        if c != "." and not c.isdigit()
    }

    # extract all numbers, indexed by position
    numbers = {
        (
            match.start(),
            y,
        ): match.group()  # note: not converting to int here in case some number contain a leading 0
        for y, line in enumerate(content.splitlines())
        for match in re.finditer(r"\d+", line)
    }

    part1 = 0
    parts = {}  # will store all parts, indexed by (y, x)
    for (x, y), num in numbers.items():
        for neighbor in neighbors(x, y, len(num)):
            if neighbor in symbols:
                part1 += int(num)
                parts[y, x] = num
                break

    part2 = 0
    for (xs, ys), symbol in symbols.items():
        if symbol != "*":
            continue

        adjacent_parts = set()
        nbs = tuple(neighbors(xs, ys, 1))
        for (yp, xp), num in parts.items():
            if yp > ys + 1:  # avoid searching parts that are below the symbol
                break
            if any((xp + d, yp) in nbs for d in range(len(num))):
                adjacent_parts.add((num, xp, yp))
                if len(adjacent_parts) > 2:  # avoid continuing the search when there are already 3 adjacent parts
                    break

        if len(adjacent_parts) == 2:
            part2 += int(adjacent_parts.pop()[0]) * int(adjacent_parts.pop()[0])

    return part1, part2


assert solve("""\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""") == (4361, 467835)

with open("03.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
