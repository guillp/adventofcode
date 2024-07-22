from collections.abc import Iterator


def solve(content: str) -> Iterator[int | str]:
    X = 1
    cycles = [X]

    for line in content.splitlines():
        if line == "noop":
            cycles.append(X)
        if line.startswith("addx"):
            n = int(line.split()[1])
            cycles.extend([X, X + n])
            X += n

    yield (
        cycles[19] * 20 + cycles[59] * 60 + cycles[99] * 100 + cycles[139] * 140 + cycles[179] * 180 + cycles[219] * 220
    )

    pixels = tuple(p % 40 - 1 <= cycles[p] <= p % 40 + 1 for p in range(240))

    for y in range(6):
        yield "".join("#" if pixels[y * 40 + x] else "." for x in range(40))


test_content = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

assert next(solve(test_content)) == 13140

with open("10.txt") as finput:
    content = finput.read()

for part in solve(content):
    print(part)
