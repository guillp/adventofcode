def holiday_ascii_string_helper_algorithm(s: str) -> int:
    v = 0
    for a in s.encode():
        v += a
        v *= 17
        v %= 256
    return v


assert holiday_ascii_string_helper_algorithm("HASH") == 52


def part1(content: str) -> int:
    return sum(holiday_ascii_string_helper_algorithm(part) for part in content.split(","))


def part2(content: str) -> int:
    boxes: list[dict[str, int]] = [{} for _ in range(256)]
    for part in content.split(","):
        if "=" in part:
            label, focal = part.split("=")
            h = holiday_ascii_string_helper_algorithm(label)
            boxes[h][label] = int(focal)
        elif "-" in part:
            label = part.rstrip("-")
            h = holiday_ascii_string_helper_algorithm(label)
            boxes[h].pop(label, None)

    return sum((i + 1) * (j + 1) * v for i, box in enumerate(boxes) for j, v in enumerate(box.values()))


test_content = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

assert part1(test_content) == 1320
assert part2(test_content) == 145

with open("15.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
