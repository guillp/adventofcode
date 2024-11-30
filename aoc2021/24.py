import re


def part1(content: str, *, part2: bool = False) -> str:
    serial = [1 if part2 else 9] * 14
    stack = []

    for i, (divz, addx, addy) in enumerate(
        re.findall(
            r"""inp w
mul x 0
add x z
mod x 26
div z (26|1)
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (\d+)
mul y x
add z y""",
            content,
            re.MULTILINE,
        ),
    ):
        if divz == "1":
            assert int(addx) >= 10
            stack.append((i, int(addy)))
        if divz == "26":
            assert int(addx) <= 0
            j, addjx = stack.pop()
            serial[i] = serial[j] + addjx + int(addx)
            if serial[i] > 9:
                serial[j] -= serial[i] - 9
                serial[i] = 9
            if serial[i] < 1:
                serial[j] += 1 - serial[i]
                serial[i] = 1

    return "".join(str(n) for n in serial)


with open("24.txt") as f:
    content = f.read()

print(part1(content))
print(part1(content, part2=True))
