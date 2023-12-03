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

symbols = {
    complex(x, y): c
    for y, line in enumerate(content.splitlines())
    for x, c in enumerate(line)
    if c != '.' and not c.isdigit()
}


def read_numbers() -> Iterator[tuple[int, int, int, int]]:
    for y, line in enumerate(content.splitlines()):
        for match in re.finditer(r'\d+', line):
            yield int(match.group()), match.start(), y, len(match.group())


def neighbors(x: int, y: int, l: int) -> Iterator[complex]:
    # 3 neighbors on the left
    yield complex(x - 1, y - 1)
    yield complex(x - 1, y)
    yield complex(x - 1, y + 1)
    # neighbors above and below
    for d in range(l):
        yield complex(x + d, y - 1)
        yield complex(x + d, y + 1)
    # 3 neighbors on the right
    yield complex(x + l, y - 1)
    yield complex(x + l, y)
    yield complex(x + l, y + 1)


s = 0
parts = set()
for number, x, y, l in read_numbers():
    for neighbor in neighbors(x, y, l):
        if neighbor in symbols:
            s += number
            parts.add((complex(x, y), l, number))
            break

print(s)

s2 = 0
for pos, symbol in symbols.items():
    if symbol != '*':
        continue

    adjacent_parts = set()
    nbs = tuple(neighbors(int(pos.real), int(pos.imag), 1))
    for origin, length, num in parts:
        if any(origin + d in nbs for d in range(length)):
            adjacent_parts.add((num, origin))

    if len(adjacent_parts) == 2:
        s2 += adjacent_parts.pop()[0] * adjacent_parts.pop()[0]

print(s2)
