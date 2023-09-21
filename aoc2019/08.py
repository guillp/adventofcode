with open("08.txt") as f:
    content = f.read()

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT

assert len(content) % LAYER_SIZE == 0

layers = [
    content[LAYER_SIZE * i : LAYER_SIZE * (i + 1)]
    for i in range(len(content) // LAYER_SIZE)
]

check = min(layers, key=lambda l: l.count("0"))

print(check.count("1") * check.count("2"))

BLACK, WHITE, TRANSPARENT = "012"

image = [next(p for p in stack if p != TRANSPARENT) for stack in zip(*layers)]
for y in range(HEIGHT):
    print("".join("# "[image[y * WIDTH + x] == BLACK] for x in range(WIDTH)))
