from collections import deque
from itertools import islice

INPUT = "768071"

def recipies():
    recipes = [3, 7]
    elf1, elf2 = 0, 1
    yield "3"
    yield "7"
    while True:
        recipe1 = recipes[elf1]
        recipe2 = recipes[elf2]
        for x in str(recipe1 + recipe2):
            recipes.append(int(x))
            yield x
        elf1 = (elf1 + recipe1 + 1) % len(recipes)
        elf2 = (elf2 + recipe2 + 1) % len(recipes)


def part1(i: int):
    return "".join(islice(recipies(), i, i+10))


def part2(sequence: str):
    d = deque(maxlen=len(sequence))
    for i, r in enumerate(recipies()):
        d.append(r)
        if "".join(d) == sequence:
            return i - len(sequence) +1


assert part1(9) == "5158916779"
assert part1(5) == "0124515891"
assert part2("51589") == 9

print(part1(int(INPUT)))
print(part2(INPUT))
