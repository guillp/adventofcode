content = """1
2
-3
3
-2
0
4
"""

with open("20.txt") as f: content = f.read()
numbers = tuple(int(x) for x in content.splitlines())


def mix(numbers: tuple[int], rounds: int = 1) -> tuple[int]:
    l = list(enumerate(numbers))
    m = len(numbers) - 1
    for _ in range(rounds):
        for i, n in enumerate(numbers):
            l.insert(((i := l.index((i, n))) + n) % m, l.pop(i))

    return tuple(n for i, n in l)


def coordinates(numbers: tuple[int]) -> int:
    zero = numbers.index(0)
    m = len(numbers)
    return numbers[(zero + 1000) % m] + numbers[(zero + 2000) % m] + numbers[(zero + 3000) % m]


print(coordinates(mix(numbers)))

print(
    coordinates(
        mix(
            tuple(x * 811589153 for x in numbers),
            10
        )
    )
)
