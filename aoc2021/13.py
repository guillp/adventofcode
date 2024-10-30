from collections.abc import Iterator


def solve(content: str) -> Iterator[int | str]:
    dots_part, folding_part = content.strip().split("\n\n")
    grid = {(int(x), int(y)) for line in dots_part.splitlines() for x, y in [line.split(",")]}
    for i, fold in enumerate(folding_part.splitlines()):
        match fold.split("="):
            case "fold along x", fold_x_:
                fold_x = int(fold_x_)
                grid = {(x, y) if x < int(fold_x) else (2 * fold_x - x, y) for x, y in grid}
            case "fold along y", fold_y_:
                fold_y = int(fold_y_)
                grid = {(x, y) if y < fold_y else (x, 2 * fold_y - y) for x, y in grid}
        if i == 0:
            yield len(grid)

    height = max(y for _, y in grid)
    width = max(x for x, _ in grid)

    for y in range(height + 1):
        yield "".join("#" if (x, y) in grid else "." for x in range(width + 1))


test_content = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

assert next(solve(test_content)) == 17

with open("13.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
