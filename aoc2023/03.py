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

symbols = {complex(x, y): c for y, line in enumerate(content.splitlines()) for x, c in enumerate(line) if
           c != '.' and not c.isdigit()}


def read_numbers() -> Iterator[tuple[int, int, int, int]]:
    clean_content = content.replace(".", " ")
    for symbol in set(symbols.values()):
        clean_content = clean_content.replace(symbol, " ")

    for y, line in enumerate(clean_content.splitlines()):
        numbers = line.split()
        i = 0  # index of the last number found in the current line
        for number in numbers:
            i += line[i:].index(number)  # increase the index to the current number
            yield int(number), i, y, len(number)
            i += len(number)  # skip to the end of the current number
            # this index trick is necessary to avoid situations where e.g index("1") returns the index of "801"


def neighbors(x: int, y: int, l: int) -> Iterator[complex]:
    # 3 neighbors on the left
    yield complex(x - 1, y - 1)
    yield complex(x - 1, y)
    yield complex(x - 1, y + 1)
    # neighbors above and below
    for d in range(l):
        yield complex(x + d, y - 1)
        yield complex(x + d, y + 1)
    # neighbors on the right
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

    surrounding = set()
    for neighbor in neighbors(int(pos.real), int(pos.imag), 1):
        for o, l, num in parts:
            if any(o + d == neighbor for d in range(l)):
                surrounding.add((num, o))

    if len(surrounding) == 2:
        s2 += surrounding.pop()[0] * surrounding.pop()[0]

print(s2)
