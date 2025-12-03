from itertools import combinations


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for line in content.strip().splitlines():

        numbers = list(line)
        while len(numbers) > 12:
            for i, number in enumerate(numbers):
                if int("".join(numbers[:-1])) < int("".join(numbers[:i] + numbers[i + 1 :])):
                    numbers = numbers[:i] + numbers[i + 1 :]
                    break
            else:
                numbers = numbers[:12]
        part2 += int("".join(numbers))

        while len(numbers) > 2:
            for i, number in enumerate(numbers):
                if int("".join(numbers[:-1])) < int("".join(numbers[:i] + numbers[i + 1 :])):
                    numbers = numbers[:i] + numbers[i + 1 :]
                    break
            else:
                numbers = numbers[:2]
        part1 += int("".join(numbers))

    return part1, part2


test_content = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""

assert solve(test_content) == (357, 3121910778619)

with open("03.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
