from collections import Counter
from collections.abc import Iterator
from itertools import pairwise


def solve(content: str) -> Iterator[int]:
    polymer, rules_part = content.strip().split("\n\n")
    rules = {
        tuple(elements): inserted for rule in rules_part.splitlines() for elements, inserted in [rule.split(" -> ")]
    }

    pairs = Counter((a, b) for a, b in pairwise(polymer))
    for step in range(40):
        for (a, b), count in tuple(pairs.items()):
            c = rules.get((a, b))
            if c:
                pairs[(a, c)] += count
                pairs[(c, b)] += count
                pairs[(a, b)] -= count
        if step + 1 == 10:
            elements_count = Counter[str]()
            for (a, b), count in pairs.items():
                elements_count[a] += count
            elements_count[polymer[-1]] += 1
            yield max(elements_count.values()) - min(elements_count.values())
    elements_count = Counter()
    for (a, b), count in pairs.items():
        elements_count[a] += count
    elements_count[polymer[-1]] += 1
    yield max(elements_count.values()) - min(elements_count.values())


test_content = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

assert tuple(solve(test_content)) == (1588, 2188189693529)

with open("14.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
