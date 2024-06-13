from functools import cache
from typing import Iterator


@cache
def next_row(content: str) -> str:
    def iter_tiles(content: str) -> Iterator[str]:
        for a, b, c in zip("." + content[:-1], content, content[1:] + ".", strict=False):
            match a, b, c:
                case "^", "^" | ".", ".":
                    yield "^"
                case ".", "^" | ".", "^":
                    yield "^"
                case _:
                    yield "."

    return "".join(iter_tiles(content))


def solve(content: str, rows: int) -> int:
    s = content.count(".")
    for _ in range(rows - 1):
        content = next_row(content)
        s += content.count(".")
    return s


assert solve(".^^.^.^^^^", 10) == 38

with open("18.txt") as f:
    content = f.read().strip()
print(solve(content, 40))
print(solve(content, 400000))
