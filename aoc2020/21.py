from collections.abc import Iterator


def solve(content: str) -> Iterator[int|str]:
    def parse() -> Iterator[tuple[set[str], set[str]]]:
        for line in content.splitlines():
            ingredients, allergens = line.rstrip(")").split(" (contains ")
            yield set(ingredients.split()), set(allergens.split(", "))


    pairs = tuple(parse())
    all_ingredients = set()
    all_allergens = set()
    for ingredients, allergens in pairs:
        all_ingredients |= ingredients
        all_allergens |= allergens

    safe_ingredients = set(all_ingredients)
    allergens_map = {}
    for allergen in all_allergens:
        candidates = set(all_ingredients)
        for ingredients, allergens in pairs:
            if allergen in allergens:
                candidates &= ingredients
        safe_ingredients -= candidates
        allergens_map[allergen] = candidates

    yield sum(len(ingredients & safe_ingredients) for ingredients, _ in pairs)

    while any(len(v) > 1 for v in allergens_map.values()):
        for allergen, candidates in allergens_map.items():
            if len(candidates) == 1:
                for other_allergen, other_candidates in allergens_map.items():
                    if len(other_candidates) > 1:
                        allergens_map[other_allergen] = other_candidates - candidates

    yield ",".join(allergens_map[allergen].pop() for allergen in sorted(allergens_map))

test_content = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

assert tuple(solve(test_content)) == (5, "mxmxvkd,sqjhc,fvjkl")

with open("21.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
