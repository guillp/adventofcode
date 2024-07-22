from collections import defaultdict

SNAFU_DIGITS = {
    "1": 1,
    "2": 2,
    "0": 0,
    "-": -1,
    "=": -2,
}

DIGITS_SNAFU = {v: k for k, v in SNAFU_DIGITS.items()}


def part1(content: str) -> str:
    power_of_fives: dict[int, int] = defaultdict(int)
    for snafu in content.splitlines():
        for i, digit in enumerate(reversed(snafu)):
            power_of_fives[i] += SNAFU_DIGITS[digit]

    total = sum(v * 5**k for k, v in power_of_fives.items())

    for k in range(max(power_of_fives)):
        v = power_of_fives[k]
        if not -2 <= v <= 2:
            div, mod = divmod(v * 5**k, 5 ** (k + 1))
            mod //= 5**k
            if mod > 2:
                div += 1
                mod -= 5
            power_of_fives[k + 1] += div
            power_of_fives[k] = mod

        assert sum(v * 5**k for k, v in power_of_fives.items()) == total, (
            sum(v * 5**k for k, v in power_of_fives.items()) - total
        )

    snafu = "".join(DIGITS_SNAFU[power_of_fives[k]] for k in range(max(power_of_fives), -1, -1))

    return snafu


test_content = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

assert part1(test_content) == "2=-1=0"

with open("25.txt") as f:
    content = f.read()

print(part1(content))
