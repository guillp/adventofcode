from collections.abc import Iterator
from itertools import combinations


def solve(content: str, n: int = 25) -> Iterator[int]:
    numbers = tuple(int(x) for x in content.strip().splitlines())
    invalid_number: int
    for i in range(n, len(numbers)):
        number = numbers[i]
        if not any(a + b == number for a, b in combinations(numbers[i - n : i], r=2)):
            invalid_number = number
            yield number
            break

    for i in range(len(numbers)):
        s = numbers[i]
        j = i + 1
        while s < invalid_number:
            s += numbers[j]
            j += 1
        if s == invalid_number:
            yield min(numbers[i:j]) + max(numbers[i:j])
            break


test_content = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

assert tuple(solve(test_content, n=5)) == (127, 62)

with open("09.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
