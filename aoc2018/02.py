from itertools import combinations


def part1(content: str) -> int:
    twos = threes = 0
    for line in content.splitlines():
        if any(line.count(letter) == 2 for letter in set(line)):
            twos += 1
        if any(line.count(letter) == 3 for letter in set(line)):
            threes += 1
    return twos * threes


def part2(content: str) -> str:
    for left, right in combinations(content.splitlines(), r=2):
        if sum(a != b for a, b in zip(left, right)) == 1:
            return "".join(a for a, b in zip(left, right) if a == b)
    assert False, "Solution not found!"


assert (
    part1("""\
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""")
    == 12
)

assert (
    part2("""\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""")
    == "fgij"
)

with open("02.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
