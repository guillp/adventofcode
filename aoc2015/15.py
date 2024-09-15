import re
from collections.abc import Iterator
from math import prod


def iter_ingredients(content: str) -> Iterator[tuple[str, tuple[int, int, int, int, int]]]:
    for name, capacity, durability, flavor, texture, calories in re.findall(
        r"(\w+?): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)",
        content,
        re.MULTILINE,
    ):
        yield (
            name,
            (
                int(capacity),
                int(durability),
                int(flavor),
                int(texture),
                int(calories),
            ),
        )


def score(
    ingredients: dict[str, tuple[int, int, int, int, int]],
    quantities: dict[str, int],
    *,
    part2: bool = False,
) -> int:
    totals = [0] * 5
    for name, properties in ingredients.items():
        for i, x in enumerate(properties):
            totals[i] += x * quantities[name]

    totals = [max(t, 0) for t in totals]
    calories = totals.pop(-1)
    if part2 and calories != 500:
        return 0
    return prod(totals)


def solve(content: str) -> Iterator[int]:
    ingredients = dict(iter_ingredients(content))

    for part2 in (False, True):
        yield max(
            score(
                ingredients,
                {
                    "Butterscotch": bu,
                    "Candy": ca,
                    "Chocolate": ch,
                    "Sprinkles": 100 - bu - ca - ch,
                },
                part2=part2,
            )
            for bu in range(100)
            for ca in range(100 - bu)
            for ch in range(100 - bu - ca)
        )


with open("15.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
