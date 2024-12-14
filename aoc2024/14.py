import re
from collections.abc import Iterator
from itertools import count


def solve(content: str, width: int = 101, height: int = 103) -> Iterator[int]:
    topleft = topright = bottomleft = bottomright = 0
    robots = []
    for line in content.strip().splitlines():
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        robots.append((x, y, vx, vy))
        xt = (x + 100 * vx) % width
        yt = (y + 100 * vy) % height
        if xt < width // 2 and yt < height // 2:
            topleft += 1
        elif xt > width // 2 and yt < height // 2:
            topright += 1
        elif xt < width // 2 and yt > height // 2:
            bottomleft += 1
        elif xt > width // 2 and yt > height // 2:
            bottomright += 1

    yield topleft * topright * bottomleft * bottomright

    for i in count():
        pixels = {((x + i * vx) % width, (y + i * vy) % height) for x, y, vx, vy in robots}
        # we're looking for a long vertical bar in the middle of the picture
        if all((width // 2, y) in pixels for y in range(height // 2, height // 2 + 10)):
            # print(f"\nAfter {i} seconds:")
            # for y in range(height):
            #    print("".join("#" if (x, y) in pixels else "." for x in range(width)))
            yield i
            return


test_content = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

assert next(solve(test_content, width=11, height=7)) == 12

with open("14.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
