from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    numbers = [int(x) for x in content.split()]
    left_list = sorted(numbers[::2])
    right_list = sorted(numbers[1::2])

    yield sum(abs(left - right) for left, right in zip(left_list, right_list))
    yield sum(left * right_list.count(left) for left in left_list)


test_content = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""

assert tuple(solve(test_content)) == (11, 31)
with open("01.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
