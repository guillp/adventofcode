def part1(content: str) -> int:
    x = y = 0
    for line in content.strip().splitlines():
        match line.split():
            case "forward", i:
                x += int(i)
            case "down", i:
                y += int(i)
            case "up", i:
                y -= int(i)
    return x * y


def part2(content: str) -> int:
    x = y = aim = 0
    for line in content.strip().splitlines():
        match line.split():
            case "forward", i:
                x += int(i)
                y += aim * int(i)
            case "down", i:
                aim += int(i)
            case "up", i:
                aim -= int(i)
    return x * y


assert (
    part1("""\
forward 5
down 5
forward 8
up 3
down 8
forward 2
""")
    == 150
)

with open("02.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
