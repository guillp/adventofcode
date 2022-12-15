from typing import Mapping

from stringparser import Parser

content = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

TARGET_Y = 10

MIN_X = MIN_Y = 0
MAX_X = MAX_Y = 20

with open('15.txt', "rt") as finput:    content = finput.read(); TARGET_Y = 2000000; MAX_X = MAX_Y = 4000000

parser = Parser("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}")

grid: Mapping[tuple[int, int], str] = {}
for line in content.splitlines():
    xs, ys, xb, yb = parser(line)
    grid[xs, ys] = "S"
    grid[xb, yb] = "B"
    d = abs(xs - xb) + abs(ys - yb)
    D = abs(ys - TARGET_Y)
    if D <= d:
        y = TARGET_Y - ys
        for x in range(d - abs(y) + 1):
            for pos in ((xs + x, ys + y), (xs - x, ys + y)):
                if pos not in grid:
                    grid[pos] = "#"

left = min(pos[0] for pos in grid)
right = max(pos[0] for pos in grid)
top = min(pos[1] for pos in grid)
bottom = max(pos[1] for pos in grid)

# for y in range(top, bottom + 1):
#    print(f'{y:02d}', "".join(grid.get((x, y), ".") for x in range(left, right + 1)))

print(sum(grid.get((x, TARGET_Y)) == '#' for x in range(left, right)))


class Frequency:
    def __init__(self, x: int):
        self.x = x
        self.candidate_y = [(MIN_Y, MAX_Y)]

    def remove(self, top, bottom):
        new_candidates = []
        for ctop, cbottom in self.candidate_y:
            if ctop < top and cbottom > bottom:  # cut the middle
                new_candidates.append((ctop, top - 1))
                new_candidates.append((bottom + 1, cbottom))
            elif top <= ctop <= bottom and cbottom > bottom:  # cut the top
                new_candidates.append((bottom + 1, cbottom))
            elif ctop < top and top <= cbottom <= bottom:  # cut the bottom
                new_candidates.append((ctop, top - 1))
            elif ctop >= top and cbottom <= bottom:  # cuts everything
                pass
            else:
                new_candidates.append((ctop, cbottom))
        #print(self.x, "before:", self.candidate_y, "after:", new_candidates)
        self.candidate_y = new_candidates

    def candidates(self):
        for top, bottom in self.candidate_y:
            for y in range(top, bottom + 1):
                yield self.x * 4000000 + y


frequencies = {x: Frequency(x) for x in range(MIN_X, MAX_X + 1)}
for line in content.splitlines():
    xs, ys, xb, yb = parser(line)
    d = abs(xs - xb) + abs(ys - yb)
    for x in range(d + 1):
        y = d - x
        if xs + x in frequencies:
            frequencies[xs + x].remove(ys - y, ys + y)
        if xs - x in frequencies:
            frequencies[xs - x].remove(ys - y, ys + y)

for x, frequency in frequencies.items():
    candidates = list(frequency.candidates())
    if candidates:
        print(candidates)
