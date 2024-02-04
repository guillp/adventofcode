import re
from typing import Iterator

with open("03.txt") as f:
    content = f.read()

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
    ): match.group()
    for y, line in enumerate(content.splitlines())
    for match in re.finditer(r"\d+", line)
}


def neighbors(x: int, y: int, l: int) -> Iterator[tuple[int, int]]:
    yield x - 1, y  # neighbor on the left
    # neighbors above and below
    for d in range(-1, l + 1):
        yield x + d, y - 1
        yield x + d, y + 1
    yield x + l, y  # neighbor on the right


s = 0
parts = {}  # will store all parts, indexed by (y, x)
for (x, y), num in numbers.items():
    for neighbor in neighbors(x, y, len(num)):
        if neighbor in symbols:
            s += int(num)
            parts[y, x] = num
            break

print(s)

s2 = 0
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
            if len(adjacent_parts) > 2:
                break  # avoid continuing the search when there are already 3 adjacent parts

    if len(adjacent_parts) == 2:
        s2 += int(adjacent_parts.pop()[0]) * int(adjacent_parts.pop()[0])

print(s2)
