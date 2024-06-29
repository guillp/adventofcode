import re
from collections import Counter
from functools import cache
from itertools import permutations


def part1(content: str) -> str:
    programs = set()
    nonroots = set()
    for line in content.splitlines():
        if " -> " in line:
            source, dests = line.split(" -> ")
            nonroots.update(dests.split(", "))
            programs.add(source.split(" ")[0])
        else:
            programs.add(line.split(" ")[0])
    return (programs - nonroots).pop()


def part2(content: str) -> int:
    G = {}
    weights = {}
    for node, weight, successors in re.findall(r"^(\w+) \((\d+)\) -> (.+)$", content, re.MULTILINE):
        G[node] = set(successors.split(", "))
        weights[node] = int(weight)
    for node, weight in re.findall(r"^(\w+) \((\d+)\)$", content, re.MULTILINE):
        weights[node] = int(weight)

    @cache
    def calc_weight(node: str) -> int:
        w = weights[node]
        if successors := G.get(node):
            for successor in successors:
                w += calc_weight(successor)
        return w

    candidates = {}
    for node, successors in G.items():
        successor_weights = {successor: calc_weight(successor) for successor in successors}
        counter = Counter(successor_weights.values())
        if len(counter) > 1:
            candidates[node] = successor_weights

    # remove candidates that are parent of another candidate, keeping only the childmost node
    for node1, node2 in permutations(candidates, 2):
        if node2 in candidates and node1 in candidates[node2]:
            del candidates[node2]

    unbalanced_parent, unbalanced_successors = candidates.popitem()
    # find the node that has a different weight than its neighbors
    (balanced_weight, _), (unbalanced_weight, _) = Counter(unbalanced_successors.values()).most_common()
    unbalanced_node = next(node for node, weight in unbalanced_successors.items() if weight == unbalanced_weight)

    return balanced_weight - sum(calc_weight(s) for s in G[unbalanced_node])


test_content = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""

assert part1(test_content) == "tknk"
assert part2(test_content) == 60

with open("07.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
