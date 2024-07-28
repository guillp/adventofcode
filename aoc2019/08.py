from collections.abc import Iterator


def solve(content: str) -> Iterator[int | str]:
    WIDTH = 25
    HEIGHT = 6
    LAYER_SIZE = WIDTH * HEIGHT

    assert len(content) % LAYER_SIZE == 0

    layers = [content[LAYER_SIZE * i : LAYER_SIZE * (i + 1)] for i in range(len(content) // LAYER_SIZE)]

    check = min(layers, key=lambda l: l.count("0"))
    yield check.count("1") * check.count("2")

    BLACK, TRANSPARENT = "0", "2"

    image = [next(p for p in stack if p != TRANSPARENT) for stack in zip(*layers)]
    for y in range(HEIGHT):
        yield "".join("# "[image[y * WIDTH + x] == BLACK] for x in range(WIDTH))


with open("08.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
