import re
from operator import itemgetter

test_content = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

with open("22.txt") as f:
    content = f.read()


def solve(content: str) -> int:
    # convert each brick to a set of cubes
    bricks = sorted(
        tuple(
            (z, x, y) # z first so bricks are sorted by initial altitude
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
            for z in range(z1, z2 + 1)
        )
        for line in content.splitlines()
        for x1, y1, z1, x2, y2, z2 in ((int(x) for x in re.findall(r"\d+", line)),)
    )

    # apply gravity to get into initial position
    gravity(bricks)

    part1 = part2 = 0
    # try to remove each brick and check if anything moves
    for i, brick in enumerate(bricks):
        bricks_minus_i = bricks[:i] + bricks[i + 1 :]
        if (move_count := gravity(bricks_minus_i)) == 0:
            part1 += 1
        part2 += move_count
    return part1, part2


def gravity(bricks: list[set[tuple[int, int, int]]]) -> int:
    floor = set()
    move_count = 0
    for i, brick in enumerate(bricks):
        moved = False
        while all(z > 1 and (z - 1, x, y) not in floor for z, x, y in brick):
            brick = {(z - 1, x, y) for z, x, y in brick}
            moved = True
        floor |= set(brick)
        if moved:
            bricks[i] = brick
            move_count += 1

    return move_count


assert solve(test_content) == (5, 7)
print(*solve(content))
