import re
from collections import defaultdict
from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    containers = defaultdict[str, dict[str, int]](dict)
    rules = defaultdict[str, dict[str, int]](dict)
    for line in content.strip().splitlines():
        recipient, inner_bags = line.split(" bags contain ")
        for qty, name in re.findall(r"(\d+) (.+?) bags?", inner_bags):
            containers[name][recipient] = int(qty)
            rules[recipient][name] = int(qty)

    pool = {"shiny gold"}
    part1 = set[str]()
    while pool:
        new_bags = set(containers[pool.pop()])
        pool |= new_bags - part1
        part1 |= new_bags

    yield len(part1)

    scores = {bag: 0 for bag in set(containers) - set(rules)}
    while set(rules) - set(scores):
        for inner_color, bags in rules.items():
            if all(outer_color in scores for outer_color, qty in bags.items()):
                scores[inner_color] = sum(qty * (scores[outer_color] + 1) for outer_color, qty in bags.items())
                if inner_color == "shiny gold":
                    yield scores[inner_color]
                    return


assert tuple(
    solve("""\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""),
) == (4, 32)


with open("07.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
