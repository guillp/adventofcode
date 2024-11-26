def part1(content: str) -> int:
    pos = 0j
    direction = 1 + 0j
    for line in content.strip().splitlines():
        match line[0], int(line[1:]):
            case "N", i:
                pos -= i * 1j
            case "S", i:
                pos += i * 1j
            case "E", i:
                pos += i
            case "W", i:
                pos -= i
            case ("L", 90) | ("R", 270):
                direction *= -1j
            case ("R", 90) | ("L", 270):
                direction *= 1j
            case "R" | "L", 180:
                direction *= -1
            case "F", i:
                pos += direction * i
            case _:
                assert False

    return int(abs(pos.real) + abs(pos.imag))


def part2(content: str) -> int:
    pos = 0j
    waypoint = 10 - 1j

    for line in content.strip().splitlines():
        match line[0], int(line[1:]):
            case "N", i:
                waypoint -= i * 1j
            case "S", i:
                waypoint += i * 1j
            case "E", i:
                waypoint += i
            case "W", i:
                waypoint -= i
            case ("L", 90) | ("R", 270):
                waypoint *= -1j
            case ("R", 90) | ("L", 270):
                waypoint *= 1j
            case "R" | "L", 180:
                waypoint *= -1
            case "F", i:
                pos += waypoint * i
            case _:
                assert False

    return int(abs(pos.real) + abs(pos.imag))


test_content = """\
F10
N3
F7
R90
F11
"""
assert part1(test_content) == 25
assert part2(test_content) == 286

with open("12.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
