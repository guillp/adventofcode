import math

with open("14.txt") as f: content = f.read()

def parse(ingredient: str) -> tuple[str, int]:
    n, material = ingredient.split(" ")
    return material, int(n)


G = {}
Q = {}
for line in content.splitlines():
    source, result = line.split(" => ")
    material, n = parse(result)
    G[material] = dict(parse(ingredient) for ingredient in source.split(", "))
    Q[material] = n

assert Q["FUEL"] == 1

def calc_ore_cost(n: int, mat: str = "FUEL") -> int:
    required = dict(G[mat])
    if n > 1:
        for material in required:
            required[material] *= n
    while True:
        for ingredient, quantity in list(required.items()):
            if quantity <= 0 or ingredient == "ORE":
                continue

            mult = math.ceil(required[ingredient]/Q[ingredient])
            required[ingredient] -= Q[ingredient] * mult
            for i, q in G[ingredient].items():
                required[i] = q * mult + required.get(i, 0)

        if all(v <= 0 or k == "ORE" for k, v in required.items()):
            break

    return required["ORE"]


ore_for_1_fuel = calc_ore_cost(1)
print(ore_for_1_fuel)

T = 1000000000000
nb_fuel = int(T / ore_for_1_fuel * (T / calc_ore_cost(T / ore_for_1_fuel)))
assert calc_ore_cost(nb_fuel) <= T < calc_ore_cost(nb_fuel + 1)
print(nb_fuel)
