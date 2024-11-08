from collections.abc import Iterator, Sequence
from itertools import product

Pixels = frozenset[tuple[int, int]]


def to_pixels(pattern: Sequence[str]) -> Pixels:
    return frozenset((x, y) for y, line in enumerate(pattern) for x, c in enumerate(line) if c == "#")


def transformations(pattern: Sequence[str]) -> Iterator[Pixels]:
    h = len(pattern) - 1
    p = to_pixels(pattern)
    yield p
    yield (p := frozenset((y, x) for x, y in p))
    yield (p := frozenset((x, h - y) for x, y in p))
    yield (p := frozenset((y, x) for x, y in p))
    yield (p := frozenset((x, h - y) for x, y in p))
    yield (p := frozenset((y, x) for x, y in p))
    yield (p := frozenset((x, h - y) for x, y in p))
    yield (p := frozenset((y, x) for x, y in p))


def part1(content: str, iterations: int = 5) -> int:
    def iter_rules() -> Iterator[tuple[int, Pixels, Pixels]]:
        for line in content.splitlines():
            src, dst = line.split(" => ")
            src_lines = src.split("/")
            dst_lines = to_pixels(dst.split("/"))
            for transformation in transformations(src_lines):
                yield len(src_lines), transformation, dst_lines

    rules2 = {}
    rules3 = {}
    for rule_len, src, dst in iter_rules():
        if rule_len == 2:
            rules2[src] = dst
        elif rule_len == 3:
            rules3[src] = dst

    grid = to_pixels(
        """\
.#.
..#
###""".splitlines(),
    )

    size = 3
    for i in range(iterations):
        new_grid = set()
        rules: dict[Pixels, Pixels]
        if size % 2 == 0:
            rules = rules2
            n = 2
        elif size % 3 == 0:
            rules = rules3
            n = 3
        else:
            assert False
        for x_sq, y_sq in product(range(size // n), repeat=2):
            before = frozenset((x, y) for x, y in product(range(n), repeat=2) if (x + x_sq * n, y + y_sq * n) in grid)
            if after := rules.get(before):
                for x, y in after:
                    new_grid.add((x_sq * (n + 1) + x, y_sq * (n + 1) + y))
        size += size // n
        grid = frozenset(new_grid)

        # for y in range(size):
        #    print("".join("#" if (x,y) in grid else "." for x in range(size)))

    return len(grid)


test_content = """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""

assert part1(test_content, 2) == 12

with open("21.txt") as f:
    content = f.read()

print(part1(content))
print(part1(content, iterations=18))
