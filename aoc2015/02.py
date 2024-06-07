def wrap(l: int, w: int, h: int) -> int:
    return 2 * l * w + 2 * w * h + 2 * h * l + min((l * w, w * h, h * l))


def part1(content: str) -> int:
    s = 0
    for box in content.splitlines():
        l, w, h = (int(x) for x in box.split("x"))
        s += wrap(l, w, h)

    return s


def ribbon(l: int, w: int, h: int) -> int:
    return sum(sorted((l, w, h))[:2]) * 2 + l * w * h


def part2(content: str) -> int:
    s2 = 0
    for box in content.splitlines():
        l, w, h = (int(x) for x in box.split("x"))
        s2 += ribbon(l, w, h)

    return s2


assert part1("2x3x4") == 58
assert part1("1x1x10") == 43


with open("02.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
