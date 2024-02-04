with open('04.txt') as f: content = f.read()


def part1(content: str) -> int:
    return sum(1 for line in content.splitlines() if len(set(line.split())) == len(line.split()))


print(part1(content))


def part2(content: str) -> int:
    return sum(1 for line in content.splitlines() if len(set("".join(sorted(word)) for word in line.split())) == len(line.split()))

print(part2(content))