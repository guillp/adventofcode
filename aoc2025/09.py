from itertools import combinations, pairwise


def to_rectangle(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int, int, int, int]:
    if x1 > x2:
        x2, x1 = x1, x2
    if y1 > y2:
        y2, y1 = y1, y2
    return (x2 - x1 + 1) * (y2 - y1 + 1), x1, y1, x2, y2


def solve(content: str) -> tuple[int, int]:
    tiles = [tuple(int(n) for n in line.split(",")) for line in content.strip().splitlines()]
    rectangles = [to_rectangle(x1, y1, x2, y2) for (x1, y1), (x2, y2) in combinations(tiles, 2)]
    rectangles.sort(key=lambda r: abs(r[0]), reverse=True)
    part1 = rectangles[0][0]

    inside = list[tuple[int, int]]()
    outside = list[tuple[int, int]]()
    clockwise = 0
    for (xa, ya), (xb, yb), (xc, yc) in zip(tiles, tiles[1:] + tiles[:1], tiles[2:] + tiles[:2]):
        if yb < ya and xc < xb:  # down then left
            inside.append((xb - 1, yb + 1))
            outside.append((xb + 1, yb - 1))
            clockwise += 1
        elif xb < xa and yc > yb:  # left then up
            inside.append((xb + 1, yb + 1))
            outside.append((xb - 1, yb - 1))
            clockwise += 1
        elif yb > ya and xc > xb:  # up then right
            inside.append((xb + 1, yb - 1))
            outside.append((xb - 1, yb + 1))
            clockwise += 1
        elif xb > xa and yc < yb:  # right then down
            inside.append((xb - 1, yb - 1))
            outside.append((xb + 1, yb + 1))
            clockwise += 1

        elif xb < xa and yc < yb:  # left then down
            outside.append((xb + 1, yb - 1))
            inside.append((xb - 1, yb + 1))
            clockwise -= 1
        elif yb < ya and xc > xb:  # down then right
            outside.append((xb + 1, yb + 1))
            inside.append((xb - 1, yb - 1))
            clockwise -= 1
        elif xb > xa and yc > yb:  # right then up
            outside.append((xb - 1, yb + 1))
            inside.append((xb + 1, yb - 1))
            clockwise -= 1
        elif yb > ya and xc < xb:  # up then left
            outside.append((xb - 1, yb - 1))
            inside.append((xb + 1, yb + 1))
            clockwise -= 1

    if clockwise < 0:
        outside, inside = inside, outside

    for area, left, bottom, right, top in rectangles:
        for (x1, y1), (x2, y2) in pairwise(outside + outside[:1]):
            if not (right < min(x1, x2) or left > max(x1, x2) or top < min(y1, y2) or bottom > max(y1, y2)):
                break
        else:
            return part1, area
    assert False


test_content = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

assert solve(test_content) == (50, 24)

with open("09.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
