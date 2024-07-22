from collections.abc import Iterator


def mix(numbers: tuple[int, ...], rounds: int = 1) -> tuple[int, ...]:
    l = list(enumerate(numbers))
    m = len(numbers) - 1
    for _ in range(rounds):
        for i, n in enumerate(numbers):
            l.insert(((i := l.index((i, n))) + n) % m, l.pop(i))

    return tuple(n for i, n in l)


def coordinates(numbers: tuple[int, ...]) -> int:
    zero = numbers.index(0)
    m = len(numbers)
    return numbers[(zero + 1000) % m] + numbers[(zero + 2000) % m] + numbers[(zero + 3000) % m]


def solve(content: str) -> Iterator[int]:
    numbers = tuple(int(x) for x in content.splitlines())
    yield coordinates(mix(numbers))
    yield coordinates(mix(tuple(x * 811589153 for x in numbers), 10))


test_content = """\
1
2
-3
3
-2
0
4
"""

assert tuple(solve(test_content)) == (3, 1623178306)
with open("20.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
