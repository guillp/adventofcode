from collections.abc import Iterator
from itertools import pairwise


def solve(content: str) -> Iterator[int]:
    reports = [tuple(int(x) for x in line.split()) for line in content.strip().splitlines()]

    yield sum(
        all((left < right and right - left <= 3) for left, right in pairwise(report))
        or all((left > right and left - right <= 3) for left, right in pairwise(report))
        for report in reports
    )

    part2 = 0
    for report in reports:
        for x in range(len(report)):
            edited_report = report[:x] + report[x + 1 :]
            if all((left < right and right - left <= 3) for left, right in pairwise(edited_report)) or all(
                (left > right and left - right <= 3) for left, right in pairwise(edited_report)
            ):
                part2 += 1
                break
    yield part2


test_content = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

assert tuple(solve(test_content)) == (2, 4)

with open("02.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
