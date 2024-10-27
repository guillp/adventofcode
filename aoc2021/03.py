from collections.abc import Iterator
from typing import Literal


def solve(content: str) -> Iterator[int]:
    numbers = tuple(content.strip().split())

    def most_common_bit(numbers: set[str], bit: int, tie: str = "1") -> Literal["0", "1"]:
        match sum(int(number[bit]) for number in numbers) - len(numbers) / 2:
            case 0:
                return tie
            case i if i < 0:
                return "0"
            case i if i > 0:
                return "1"
            case _:
                assert False

    gamma_bits = "".join(x for bit in range(len(numbers[0])) for x in most_common_bit(set(numbers), bit, "1"))
    gamma = int(gamma_bits, 2)
    epsilon = ~gamma % 2 ** len(numbers[0])
    yield gamma * epsilon

    possible_oxygen = set(numbers)
    possible_co2 = set(numbers)
    for i in range(len(numbers[0])):
        if len(possible_oxygen) > 1:
            mcb = most_common_bit(possible_oxygen, i, "1")
            for number in tuple(possible_oxygen):
                if number[i] != mcb:
                    possible_oxygen.remove(number)

        if len(possible_co2) > 1:
            mcb = most_common_bit(possible_co2, i, "1")
            for number in tuple(possible_co2):
                if number[i] == mcb:
                    possible_co2.remove(number)

        if len(possible_oxygen) == len(possible_co2) == 1:
            break

    yield int(possible_oxygen.pop(), 2) * int(possible_co2.pop(), 2)


assert tuple(
    solve("""\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""),
) == (198, 230)

with open("03.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
