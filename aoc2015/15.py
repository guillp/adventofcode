from stringparser import Parser
import pandas as pd

with open('15.txt', "rt") as finput:
    content = finput.read()

parser = Parser(
    "{name}: capacity {capacity:d}, durability {durability:d}, flavor {flavor:d}, texture {texture:d}, calories {calories:d}")

ingredients = pd.DataFrame(parser(line) for line in content.splitlines()).assign(
    name=lambda df: df.name.str.lower()).set_index('name')

print(ingredients)


def score(**ing: int):
    s = pd.Series(0, index=ingredients.columns)
    for name, quantity in ing.items():
        s += ingredients.loc[name.lower()] * quantity

    s = s.apply(lambda x: max(x, 0))
    del s['calories']
    return s.prod()


print(max(
    score(butterscotch=bu, candy=ca,chocolate=ch, sprinkles=100-bu-ca-ch)
    for bu in range(100)
    for ca in range(100-bu)
    for ch in range(100-bu-ca)
))


def score_with_500_cal(**ing: int):
    s = pd.Series(0, index=ingredients.columns)
    for name, quantity in ing.items():
        s += ingredients.loc[name.lower()] * quantity

    s = s.apply(lambda x: max(x, 0))
    if s['calories'] != 500:
        return 0
    del s['calories']
    return s.prod()

print(max(
    score_with_500_cal(butterscotch=bu, candy=ca,chocolate=ch, sprinkles=100-bu-ca-ch)
    for bu in range(100)
    for ca in range(100-bu)
    for ch in range(100-bu-ca)
))