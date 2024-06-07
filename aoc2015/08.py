import json


def part1(content: str) -> int:
    return sum(len(line) - len(eval(line)) for line in content.splitlines())


def part2(content: str) -> int:
    return sum(len(json.dumps(line)) - len(line) for line in content.splitlines())


with open("08.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
