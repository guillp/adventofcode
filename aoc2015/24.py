import math
from itertools import combinations

with open("24.txt", "rt") as finput:
    content = finput.read()

weights = [int(line) for line in content.splitlines()]

total_weight = sum(weights)
group1 = min(
    (
        comb
        for i in range(len(weights))
        for comb in combinations(weights, i)
        if sum(comb) == total_weight // 3
    ),
    key=math.prod,
)
print(math.prod(group1))

group1 = min(
    (
        comb
        for i in range(len(weights))
        for comb in combinations(weights, i)
        if sum(comb) == total_weight // 4
    ),
    key=lambda g: (len(g), math.prod(g)),
)
print(math.prod(group1))
