with open('01.txt') as f: content = f.read()


def fuel(mass: int) -> int:
    return int(mass / 3 - 2)


part1 = sum(fuel(int(line)) for line in content.split())
print(part1)

part2 = 0
for line in content.splitlines():
    required_fuel = fuel(int(line))
    while required_fuel > 0:
        part2 += required_fuel
        required_fuel = fuel(required_fuel)

print(part2)