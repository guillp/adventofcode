from functools import cache
from typing import Iterable


@cache
def next_row(content: str) -> Iterable[str]:
    def iter(content):
        for a,b,c in zip("."+content[:-1], content, content[1:]+"."):
            match a, b, c:
                case "^", "^"|".", ".":
                    yield "^"
                case ".", "^"|".", "^":
                    yield "^"
                case _:
                    yield "."

    return "".join(iter(content))

def solve(content: str, rows) -> int:
    s = content.count(".")
    for _ in range(rows-1):
        content = next_row(content)
        s+= content.count(".")
    return s

assert solve(".^^.^.^^^^", 10) == 38

with open("18.txt") as f: content = f.read().strip()
print(solve(content, 40))
print(solve(content, 400000))