import re
from typing import Iterator

content = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

with open('03.txt') as f: content = f.read()

# extract each symbol from input, indexed by position
symbols = {
    (x, y): c
    for y, line in enumerate(content.splitlines())
    for x, c in enumerate(line)
    if c != '.' and not c.isdigit()
}

# extract all numbers, indexed by position
numbers = {
    (match.start(), y): match.group()  # note: not converting to int here in case some number contain a leading 0
    for y, line in enumerate(content.splitlines())
    for match in re.finditer(r'\d+', line)
}


def neighbors(x: int, y: int, l: int) -> Iterator[tuple[int, int]]:
    # 3 neighbors on the left
    yield x - 1, y - 1
    yield x - 1, y
    yield x - 1, y + 1
    # neighbors above and below
    for d in range(l):
        yield x + d, y - 1
        yield x + d, y + 1
    # 3 neighbors on the right
    yield x + l, y - 1
    yield x + l, y
    yield x + l, y + 1


s = 0
parts = set()
for (x, y), num in numbers.items():
    for neighbor in neighbors(x, y, len(num)):
        if neighbor in symbols:
            s += int(num)
            parts.add((x, y, num))
            break

print(s)

s2 = 0
for (xs, ys), symbol in symbols.items():
    if symbol != '*':
        continue

    adjacent_parts = set()
    nbs = tuple(neighbors(xs, ys, 1))
    for xp, yp, num in parts:
        if any((xp + d, yp) in nbs for d in range(len(num))):
            adjacent_parts.add((num, xp, yp))
            if len(adjacent_parts) > 2:
                break

    if len(adjacent_parts) == 2:
        s2 += int(adjacent_parts.pop()[0]) * int(adjacent_parts.pop()[0])

print(s2)
