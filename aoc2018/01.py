from itertools import cycle


def part1(content: str) -> int:
    return sum(int(n) for n in content.splitlines())


def part2(content: str) -> int:
    current = 0
    reached = set()
    for line in cycle(content.splitlines()):
        current += int(line)
        if current in reached:
            return current
        reached.add(current)
    assert False, "Solution not found!"


with open("01.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
