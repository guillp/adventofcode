import re


def part1(content: str) -> int:
    s = 0
    for line in content.strip().splitlines():
        numbers = re.findall(r"\d", line)
        s += 10 * int(numbers[0])
        s += int(numbers[-1])

    return s


def part2(content: str) -> int:
    d = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    s = 0
    for line in content.splitlines():
        first = re.search(r"(one|two|three|four|five|six|seven|eight|nine|\d)", line).group()  # type: ignore[union-attr]
        last = re.search(r"(eno|owt|eerht|ruof|evif|xis|neves|thgie|enin|\d)", line[::-1]).group()[::-1]  # type: ignore[union-attr]

        s += 10 * (d.get(first) or int(first))
        s += d.get(last) or int(last)

    return s


assert (
    part1("""\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")
    == 142
)


assert (
    part2("""\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""")
    == 281
)

with open("01.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
