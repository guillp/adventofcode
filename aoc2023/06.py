from math import ceil, floor


def solve(t: int, d: int) -> int:
    # t is the total duration
    # d is the record distance
    # x is the number of seconds to press the button
    # we want to solve x(t-x) >= d+1
    # which is equivalent to: -x²+xt - (d+1) > 0
    # use Bhaskara to solve that 2nd degree equation
    D = t**2 - 4 * +(d + 1)
    assert D >= 0
    x1: int = ceil((t - D**0.5) / 2)
    x2: int = floor((t + D**0.5) / 2)
    return x2 - x1 + 1


def part1(content: str) -> int:
    lines = content.strip().splitlines()
    times = (int(x) for x in lines[0].split()[1:])
    distance = (int(x) for x in lines[1].split()[1:])

    s = 1
    for t, d in zip(times, distance, strict=False):
        s *= solve(t, d)
    return s


def part2(content: str) -> int:
    lines = content.splitlines()
    t = int("".join(lines[0].split()[1:]))
    d = int("".join(lines[1].split()[1:]))
    return solve(t, d)


test_content = """\
Time:      7  15   30
Distance:  9  40  200
"""

assert part1(test_content) == 288
assert part2(test_content) == 71503

with open("06.txt") as f:
    content = f.read()


print(part1(content))
print(part2(content))
