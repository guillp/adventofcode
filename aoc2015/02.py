with open("02.txt", "rt") as finput:
    content = finput.read()


def wrap(l: int, w: int, h: int) -> int:
    return 2 * l * w + 2 * w * h + 2 * h * l + min((l * w, w * h, h * l))


s = 0
for box in content.splitlines():
    l, w, h = [int(x) for x in box.split("x")]
    s += wrap(l, w, h)

print(s)


def ribbon(l, w, h) -> int:
    return sum(sorted((l, w, h))[:2]) * 2 + l * w * h


s2 = 0
for box in content.splitlines():
    l, w, h = [int(x) for x in box.split("x")]
    s2 += ribbon(l, w, h)

print(s2)
