from itertools import permutations
from typing import Sequence

from stringparser import Parser
with open('13.txt', "rt") as finput:
    content = finput.read()

parser = Parser("{} would {} {:d} happiness units by sitting next to {}.")


gains = {}
for line in content.splitlines():
    a,b,c,d = parser(line)
    if b == "gain":
        gains[(a,d)] = c
    elif b == "lose":
        gains[(a,d)] = -c


def score(table: Sequence[str]) -> int:
    s = 0
    for a,b in zip(table, table[1:]+table[:1]):
        s += gains[(a,b)] + gains[(b,a)]
    return s

best_table = max(permutations(set(gain[0] for gain in gains)), key=score)
best_score = score(best_table)
print(best_score)

candidates = {gains[(a,b)] + gains[(b,a)]: (a,b)  for a,b in zip(best_table, best_table[1:]+best_table[:1])}
print(best_score - min(candidates))


