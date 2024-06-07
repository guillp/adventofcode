from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    yield content.count("(") - content.count(")")

    f = 0
    for i, c in enumerate(content):
        if c == "(":
            f += 1
        elif c == ")":
            f -= 1
        if f < 0:
            yield i + 1
            return


assert next(solve("(())")) == 0
assert next(solve("()()")) == 0
assert next(solve("(((")) == 3
assert tuple(solve("())")) == (-1, 3)
assert tuple(solve(")())())")) == (-3, 1)

with open("01.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
