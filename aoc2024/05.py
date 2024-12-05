from collections import defaultdict
from functools import cmp_to_key


def solve(content: str) -> tuple[int, int]:
    rules_part, updates_part = content.strip().split("\n\n")
    predecessors = defaultdict(set)
    for r in rules_part.splitlines():
        before, after = r.split("|")
        predecessors[int(after)].add(int(before))

    def sortorder(left: int, right: int) -> int:
        if right in predecessors[left]:
            return -1
        return 0

    part1 = part2 = 0
    for update in updates_part.splitlines():
        pages = [int(x) for x in update.split(",")]
        seen = set[int]()
        for page in pages:
            required_pages = predecessors.get(page, set())
            if any(predecessor in pages and predecessor not in seen for predecessor in required_pages):
                fixed = sorted(pages, key=cmp_to_key(sortorder))
                part2 += fixed[len(fixed) // 2]
                break
            seen.add(page)
        else:
            assert len(pages) % 2 == 1
            part1 += pages[len(pages) // 2]

    return part1, part2


test_content = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
assert tuple(solve(test_content)) == (143, 123)

with open("05.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
