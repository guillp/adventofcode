
def part1(content: str) -> int:
    return sum(
        1
        for line in content.splitlines()
        if len(set(line.split())) == len(line.split())
    )



assert part1("aa bb cc dd ee") == 1
assert part1("aa bb cc dd aa") == 0
assert part1("aa bb cc dd aaa") == 1


def part2(content: str) -> int:
    return sum(
        1
        for line in content.splitlines()
        if len(set("".join(sorted(word)) for word in line.split())) == len(line.split())
    )



assert part2("abcde fghij") == 1
assert part2("abcde xyz ecdab") == 0
assert part2("a ab abc abd abf abj") == 1
assert part2("iiii oiii ooii oooi oooo") == 1
assert part2("oiii ioii iioi iiio") == 0

with open("04.txt") as f:
    content = f.read()


print(part1(content))
print(part2(content))
