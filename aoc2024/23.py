from collections.abc import Iterator
from itertools import combinations


def solve(content: str) -> Iterator[int | str]:
    graph = dict[str, set[str]]()
    for line in content.strip().splitlines():
        left, right = line.split("-")
        graph.setdefault(left, set()).add(right)
        graph.setdefault(right, set()).add(left)

    pool = graph.copy()
    groups_of_3 = set[frozenset[str]]()
    groups_by_size = dict[int, set[frozenset[str]]]()
    while pool:
        computer, connected = pool.popitem()
        # for a group of 3, 2 elements connected to `computer` must also be connected together.
        for left, right in combinations(connected, 2):
            if left in graph[right]:
                groups_of_3.add(frozenset({computer, left, right}))

        # Detect biggest possible group by calculating the number of relations that each element has.
        # If the group is fully connected, each element has the same number of connections.
        # Otherwise, remove the least connected element and try again.
        group = {computer, *connected}
        while group:
            connections = {element: sum(element in graph[other] for other in group - {element}) for element in group}
            if all(v == len(group) - 1 for v in connections.values()):
                groups_by_size.setdefault(sum(connections.values()), set()).add(frozenset(group))
                break
            group.remove(min(connections))

    yield sum(any(computer[0] == "t" for computer in group) for group in groups_of_3)

    biggest_group = groups_by_size[max(groups_by_size)].pop()
    yield ",".join(sorted(biggest_group))


test_content = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

assert tuple(solve(test_content)) == (7, "co,de,ka,ta")

with open("23.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
