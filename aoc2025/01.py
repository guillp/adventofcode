def solve(content: str) -> tuple[int, int]:
    dial = 50
    part1 = part2 = 0

    for line in content.strip().splitlines():
        direction = line[0]
        clicks = int(line[1:])

        ticks, mod = divmod(clicks, 100)  # nb of full rotations + remaining

        if direction == "R":
            if dial + mod >= 100:  # if remaining goes past 100
                ticks += 1
            dial += mod
        elif direction == "L":
            if dial - mod <= 0 and dial != 0:  # if remaining goes past 0
                ticks += 1
            dial -= mod

        dial %= 100

        if dial == 0:
            part1 += 1
        part2 += ticks

        # print(f"The dial is rotated {line} to point at {dial}; {ticks} time, {part2} total")
    return part1, part2


test_content = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

assert solve(test_content) == (3, 6)

assert solve("R1000") == (0, 10)
assert solve("L1000") == (0, 10)
assert solve("R50") == (1, 1)
assert solve("L50") == (1, 1)

with open("01.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
