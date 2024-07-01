import string


def part1(content: str) -> int:
    s = 0
    for ruckshack in content.splitlines():
        first_half, second_half = (
            ruckshack[: len(ruckshack) // 2],
            ruckshack[len(ruckshack) // 2 :],
        )
        first_set = set(first_half)
        second_set = set(second_half)
        misplaced = (first_set & second_set).pop()
        priority = (string.ascii_lowercase + string.ascii_uppercase).index(misplaced) + 1
        s += priority

    return s


def part2(content: str) -> int:
    s = 0
    ruckshacks = content.splitlines()
    for i in range(0, len(ruckshacks), 3):
        elf1 = set(ruckshacks[i])
        elf2 = set(ruckshacks[i + 1])
        elf3 = set(ruckshacks[i + 2])
        common = (elf1 & elf2 & elf3).pop()
        priority = (string.ascii_lowercase + string.ascii_uppercase).index(common) + 1
        s += priority

    return s


test_content = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


assert part1(test_content) == 157
assert part2(test_content) == 70

with open("03.txt") as finput:
    content = finput.read()

print(part1(content))
print(part2(content))
