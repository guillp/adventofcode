import re
from collections.abc import Iterator


def codes() -> Iterator[int]:
    code = 20151125
    while True:
        yield code
        code *= 252533
        code %= 33554393


def solve(content: str) -> int:
    row, column = map(int, re.findall(r"\d+", content))
    target = sum(n for n in range(row + column - 1)) + column - 1

    return next(code for i, code in enumerate(codes()) if i == target)


with open("25.txt") as f:
    content = f.read()
print(solve(content))
