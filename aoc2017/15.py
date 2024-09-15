import re
from collections.abc import Iterable


def part1(
    content: str,
    factor_a: int = 16807,
    factor_b: int = 48271,
    modulo: int = 2147483647,
    nb: int = 40_000_000,
) -> int:
    start_a, start_b = map(int, re.findall(r"\d+", content))

    def generator(start: int, factor: int, modulo: int) -> Iterable[int]:
        while True:
            start *= factor
            start %= modulo
            yield start

    gen_a = generator(start_a, factor_a, modulo)
    gen_b = generator(start_b, factor_b, modulo)
    return sum(1 for a, b, i in zip(gen_a, gen_b, range(nb)) if a % 2**16 == b % 2**16)


def part2(
    content: str,
    factor_a: int = 16807,
    factor_b: int = 48271,
    modulo: int = 2147483647,
    nb: int = 5_000_000,
) -> int:
    start_a, start_b = map(int, re.findall(r"\d+", content))

    def generator(start: int, factor: int, modulo: int, multiple: int) -> Iterable[int]:
        while True:
            start *= factor
            start %= modulo
            if start % multiple == 0:
                yield start

    gen_a = generator(start_a, factor_a, modulo, 4)
    gen_b = generator(start_b, factor_b, modulo, 8)
    return sum(1 for a, b, i in zip(gen_a, gen_b, range(nb)) if a % 2**16 == b % 2**16)


assert part1("65 8921") == 588
assert part2("65 8921") == 309

with open("15.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
