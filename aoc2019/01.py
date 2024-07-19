def fuel(mass: int) -> int:
    return int(mass / 3 - 2)


def part1(content: str) -> int:
    return sum(fuel(int(line)) for line in content.split())


def part2(content: str) -> int:
    part2 = 0
    for line in content.splitlines():
        required_fuel = fuel(int(line))
        while required_fuel > 0:
            part2 += required_fuel
            required_fuel = fuel(required_fuel)

    return part2


assert part1("12") == 2
assert part1("14") == 2
assert part1("1969") == 654
assert part1("100756") == 33583

with open("01.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
