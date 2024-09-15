import re
from collections.abc import Iterable, Iterator


def iter_instructions(content: str) -> Iterable[tuple[str, int, int, int, int]]:
    for instruction, *coords in re.findall(
        r"^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)$",
        content,
        re.MULTILINE,
    ):
        x1, y1, x2, y2 = map(int, coords)
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        yield instruction, x1, y1, x2, y2


def solve(content: str) -> Iterator[int]:
    instructions = list(iter_instructions(content))

    lights = [False for _ in range(1000 * 1000)]
    for instruction, x1, y1, x2, y2 in instructions:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if instruction == "turn on":
                    lights[y * 1000 + x] = True
                elif instruction == "turn off":
                    lights[y * 1000 + x] = False
                elif instruction == "toggle":
                    lights[y * 1000 + x] = not lights[y * 1000 + x]

    yield sum(lights)

    lights2 = [0 for _ in range(1000 * 1000)]
    for instruction, x1, y1, x2, y2 in instructions:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if instruction == "turn on":
                    lights2[y * 1000 + x] += 1
                elif instruction == "turn off":
                    if lights2[y * 1000 + x] > 0:
                        lights2[y * 1000 + x] -= 1
                elif instruction == "toggle":
                    lights2[y * 1000 + x] += 2

    yield sum(lights2)


with open("06.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
