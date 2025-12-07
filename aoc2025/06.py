from collections.abc import Iterator
from math import prod


def part1(content: str) -> int:
    *operands, operators = content.splitlines()
    operations = dict[int, list[int]]()
    for line in operands:
        for i, number in enumerate(line.split()):
            operations.setdefault(i, []).append(int(number))

    return sum(
        sum(numbers) if operator == "+" else prod(numbers)
        for numbers, operator in zip(operations.values(), operators.split())
    )


def part2(content: str) -> int:
    *lines, operators = content.splitlines()

    total = 0
    for x, operator in enumerate(operators):
        if operator == " ":
            continue

        def iter_numbers(x: int) -> Iterator[int]:
            for i in range(x, len(lines[0])):
                chars = "".join(line[i] for line in lines).strip()
                if not chars:
                    return
                yield int(chars)

        numbers = list(iter_numbers(x))
        if operator == "+":
            total += sum(numbers)
        elif operator == "*":
            total += prod(numbers)

    return total


test_content = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""  # noqa: W291

assert part1(test_content) == 4277556
assert part2(test_content) == 3263827

with open("06.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
