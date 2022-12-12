from itertools import combinations

with open('17.txt', "rt") as finput:
    content = finput.read()

TARGET = 150
containers = tuple(sorted(int(x) for x in content.splitlines()))
print(containers)

print(sum(sum(comb) == 150 for i in range(len(containers)) for comb in combinations(containers, i)))
m = min(i for i in range(len(containers)) for comb in combinations(containers, i) if sum(comb) == 150)
print(sum(sum(comb) == 150 for comb in combinations(containers, m)))
