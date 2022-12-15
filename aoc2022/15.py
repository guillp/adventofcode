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

with open("15.txt", "rt") as finput:
    content = finput.read()
    TARGET_Y = 2000000
    MAX_X = MAX_Y = 4000000

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

print(sum(grid.get((x, TARGET_Y)) == "#" for x in range(left, right)))


class Frequency:
    def __init__(self, x: int):
        self.x = x
        self.y_candidate_ranges = [(MIN_Y, MAX_Y)]

    def remove(self, top, bottom):
        new_candidates = []
        for ctop, cbottom in self.y_candidate_ranges:
            if ctop < top and cbottom > bottom:  # cut the middle
                new_candidates.append((ctop, top - 1))
                new_candidates.append((bottom + 1, cbottom))
            elif top <= ctop <= bottom < cbottom:  # cut the top
                new_candidates.append((bottom + 1, cbottom))
            elif ctop < top <= cbottom <= bottom:  # cut the bottom
                new_candidates.append((ctop, top - 1))
            elif ctop >= top and cbottom <= bottom:  # cut everything
                pass
            else:  # cut nothing
                new_candidates.append((ctop, cbottom))
        self.y_candidate_ranges = new_candidates

    def candidates(self):
        for top, bottom in self.y_candidate_ranges:
            for y in range(top, bottom + 1):
                yield self.x * 4000000 + y

    def __bool__(self):
        return len(self.y_candidate_ranges) > 0


frequencies = {x: Frequency(x) for x in range(MIN_X, MAX_X + 1)}
for line in content.splitlines():
    xs, ys, xb, yb = parser(line)
    d = abs(xs - xb) + abs(ys - yb)

    for xd in range(d + 1):
        yd = d - xd
        for x in {xs + xd, xs - xd}:
            if x in frequencies:
                frequencies[x].remove(ys - yd, ys + yd)
                if not frequencies[x]:
                    del frequencies[x]

candidates = {x: list(frequency.candidates()) for x, frequency in frequencies.items()}
if len(candidates) > 1:
    print("Multiple candidates found!", candidates)
x, frequencies = candidates.popitem()
if len(frequencies) > 1:
    print("Multiple candidates found at x=", x, candidates)
print(frequencies[0])
