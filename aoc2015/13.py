from itertools import permutations
from typing import Sequence

from stringparser import Parser

content = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""
with open('13.txt', "rt") as finput:
    content = finput.read()

parser = Parser("{} would {} {:d} happiness units by sitting next to {}.")

gains = {}
for line in content.splitlines():
    a, b, c, d = parser(line)
    if b == "gain":
        gains[(a, d)] = c
    elif b == "lose":
        gains[(a, d)] = -c


def score(table: Sequence[str]) -> int:
    s = 0
    for a, b in zip(table, table[1:] + table[:1]):
        s += gains[(a, b)] + gains[(b, a)]
    return s


best_table = max(permutations(set(gain[0] for gain in gains)), key=score)
best_score = score(best_table)
print(best_score)

candidates = {gains[(a, b)] + gains[(b, a)]: (a, b) for a, b in zip(best_table, best_table[1:] + best_table[:1])}
print(best_score - min(candidates))
