from collections import defaultdict
from collections.abc import Iterator
from itertools import pairwise


def steps(secret: int, n: int = 2000) -> Iterator[int]:
    for i in range(n):
        secret = ((secret << 6) ^ secret) % 16777216
        secret = ((secret >> 5) ^ secret) % 16777216
        secret = ((secret << 11) ^ secret) % 16777216
        yield secret


def part1(content: str) -> int:
    return sum(tuple(steps(int(line)))[-1] for line in content.strip().splitlines())


def part2(content: str) -> int:
    prices = {
        int(seller): [int(seller)] + [price % 10 for price in steps(int(seller))]
        for seller in content.strip().splitlines()
    }
    sequences = {seller: [right - left for left, right in pairwise(prices[seller])] for seller in prices}

    best_price = {
        seller: {tuple(sequences[seller][-i - 4 : -i]): prices[seller][-i - 1] for i in range(1, 2001 - 4)}
        for seller in sequences
    }

    best_total = defaultdict[tuple[int, ...], int](int)
    for sequences2price in best_price.values():
        for sequence, price in sequences2price.items():
            best_total[sequence] += price

    return max(best_total.values())


test_content = """\
1
10
100
2024
"""

test_content2 = """\
1
2
3
2024
"""

assert part1(test_content) == 37327623
assert part2(test_content2) == 23


with open("22.txt") as f:
    content = f.read()


print(part1(content))
print(part2(content))
