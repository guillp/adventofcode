from collections import deque
from itertools import accumulate
from operator import xor


def part1(content: str, nb: int = 256) -> int:
    numbers = deque(range(nb))
    skip_size = 0
    lengths = [int(x) for x in content.strip().split(",")]

    for length in lengths:
        numbers = deque(list(reversed([numbers.popleft() for _ in range(length)])) + list(numbers))
        numbers.rotate(-length - skip_size)
        skip_size += 1

    numbers.rotate(sum(lengths) + sum(range(skip_size)))
    return numbers[0] * numbers[1]


def part2(content: str, nb: int = 256, rounds: int = 64) -> str:
    numbers = deque(range(nb))
    skip_size = 0
    lengths = [ord(x) for x in content.strip()] + [17, 31, 73, 47, 23]

    for _ in range(rounds):
        for length in lengths:
            numbers = deque(list(reversed([numbers.popleft() for _ in range(length)])) + list(numbers))
            numbers.rotate(-length - skip_size)
            skip_size += 1

    numbers.rotate(sum(lengths) * rounds + sum(range(skip_size)))
    numbers_lst = list(numbers)

    return "".join(f"{tuple(accumulate(numbers_lst[i*16:(i+1)*16], xor))[-1]:02x}" for i in range(16))


assert part1("3,4,1,5", 5) == 12

assert part2("") == "a2582a3a0e66e6e86e3812dcb672a272"

with open("10.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
