from collections import deque
from collections.abc import Iterator
from itertools import islice


def recipies() -> Iterator[str]:
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


def part1(content: str) -> str:
    i = int(content)
    return "".join(islice(recipies(), i, i + 10))


def part2(content: str) -> int:
    d: deque[str] = deque(maxlen=len(content))
    for i, r in enumerate(recipies()):
        d.append(r)
        if "".join(d) == content:
            return i - len(content) + 1
    assert False


assert part1("9") == "5158916779"
assert part1("5") == "0124515891"
assert part2("51589") == 9


INPUT = "768071"

print(part1(INPUT))
print(part2(INPUT))
