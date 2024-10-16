from collections.abc import Iterator


def react(polymer: bytes) -> int:
    i = 0
    while 0 <= i < len(polymer) - 1:
        left, right = polymer[i : i + 2]
        if abs(left - right) == 32:
            polymer = polymer[:i] + polymer[i + 2 :]
            if i > 0:
                i -= 1
        else:
            i += 1
    return len(polymer)


def solve(content: str) -> Iterator[int]:
    polymer = content.strip().encode()
    yield react(polymer)
    part2 = len(polymer)
    for letter in "abcdefghijklmnopqrstuvwxyz":
        part2 = min(part2, react(polymer.replace(letter.lower().encode(), b"").replace(letter.upper().encode(), b"")))
    yield part2


assert tuple(solve("dabAcCaCBAcCcaDA")) == (10, 4)

with open("05.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
