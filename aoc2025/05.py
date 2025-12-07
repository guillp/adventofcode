from collections.abc import Iterator
from itertools import combinations


def solve(content: str) -> Iterator[int]:
    ranges_part, ingredients_part = content.split("\n\n")

    def str_to_range(r: str) -> tuple[int, int]:
        left, right = r.split("-")
        return int(left), int(right)

    ranges = {str_to_range(range_) for range_ in ranges_part.splitlines()}

    yield sum(
        any(left <= ingredient <= right for left, right in ranges)
        for ingredient in map(int, ingredients_part.splitlines())
    )

    while True:
        for (left1, right1), (left2, right2) in combinations(ranges, 2):
            if left2 > right1 or left1 > right2:  # no overlap
                pass
            elif left1 <= left2 and right1 >= right2:  # 2 inside 1
                ranges.remove((left2, right2))
                break
            elif left2 <= left1 and right2 >= right1:  # 1 inside 2
                ranges.remove((left1, right1))
                break
            elif left1 <= left2 and right1 <= right2:  # overlap on the right
                ranges.remove((left1, right1))
                ranges.remove((left2, right2))
                ranges.add((left1, right2))
                break
            elif left2 <= left1 and right2 <= right1:  # overlap on the left
                ranges.remove((left1, right1))
                ranges.remove((left2, right2))
                ranges.add((left2, right1))
                break
            else:
                assert False
        else:
            break

    yield sum(right - left + 1 for left, right in ranges)


test_content = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

assert tuple(solve(test_content)) == (3, 14)

with open("05.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
