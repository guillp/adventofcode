def hash(s: str) -> int:
    v = 0
    for a in s.encode():
        v += a
        v *= 17
        v %= 256
    return v


assert hash("HASH") == 52

with open("15.txt") as f:
    content = f.read()
test_content = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def part1(content: str) -> int:
    return sum(hash(part) for part in content.split(","))


assert part1(test_content) == 1320
print(part1(content))


def part2(content: str):
    boxes = [{} for _ in range(256)]
    for part in content.split(","):
        if "=" in part:
            label, focal = part.split("=")
            h = hash(label)
            boxes[h][label] = int(focal)
        elif "-" in part:
            label = part.rstrip("-")
            h = hash(label)
            boxes[h].pop(label, None)

    return sum(
        (i + 1) * (j + 1) * v for i, box in enumerate(boxes) for j, v in enumerate(box.values())
    )


assert part2(test_content) == 145
print(part2(content))
