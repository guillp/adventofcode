from collections.abc import Iterator
from functools import cache
from itertools import pairwise


def solve(content: str) -> Iterator[int]:
    adapters = tuple(sorted(int(x) for x in content.strip().splitlines()))
    diff1 = diff3 = 0
    device_joltage = max(adapters) + 3
    all_nodes = (0, *adapters, device_joltage)
    for a, b in pairwise(all_nodes):
        match b - a:
            case 1:
                diff1 += 1
            case 3:
                diff3 += 1
            case _:
                assert False
    yield diff1 * diff3

    successors = {
        adapter: {successor for successor in all_nodes if adapter < successor <= adapter + 3} for adapter in all_nodes
    }

    @cache
    def count_arrangements(n: int) -> int:
        return sum(count_arrangements(successor) for successor in successors[n]) or 1

    yield count_arrangements(0)


test_content1 = """\
16
10
15
5
1
11
7
19
6
12
4
"""

test_content2 = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""

assert tuple(solve(test_content1)) == (35, 8)
assert tuple(solve(test_content2)) == (220, 19208)

with open("10.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
