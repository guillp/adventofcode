import string

content = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

with open("03.txt", "rt") as finput:
    content = finput.read()

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

print(s)

s2 = 0
ruckshacks = content.splitlines()
for i in range(0, len(ruckshacks), 3):
    elf1 = set(ruckshacks[i])
    elf2 = set(ruckshacks[i + 1])
    elf3 = set(ruckshacks[i + 2])
    common = (elf1 & elf2 & elf3).pop()
    priority = (string.ascii_lowercase + string.ascii_uppercase).index(common) + 1
    s2 += priority

print(s2)
