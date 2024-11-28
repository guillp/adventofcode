import re


def part1(content: str) -> int:
    earliest, *buses = (int(x) for x in re.findall(r"\d+", content, re.MULTILINE))
    bus = min(buses, key=lambda b: -earliest % b)
    return bus * (-earliest % bus)


def part2(content: str) -> int:
    buses = tuple((int(x), i) for i, x in enumerate(content.splitlines()[1].split(",")) if x != "x")
    departure, step = 0, 1
    for bus, offset in buses:
        while (departure + offset) % bus:
            departure += step
        step *= bus
    return departure


with open("13.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
