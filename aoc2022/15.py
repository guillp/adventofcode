import re
from collections.abc import Iterator


def solve(content: str, target_y: int = 2000000, max_x: int = 4000000, max_y: int = 4000000) -> Iterator[int]:
    grid: dict[tuple[int, int], str] = {}
    for line in content.strip().splitlines():
        xs, ys, xb, yb = (int(x) for x in re.findall(r"-?\d+", line))
        grid[xs, ys] = "S"
        grid[xb, yb] = "B"
        d = abs(xs - xb) + abs(ys - yb)
        if abs(ys - target_y) <= d:
            y = target_y - ys
            for x in range(d - abs(y) + 1):
                for pos in ((xs + x, ys + y), (xs - x, ys + y)):
                    if pos not in grid:
                        grid[pos] = "#"

    left = min(pos[0] for pos in grid)
    right = max(pos[0] for pos in grid)

    # top = min(pos[1] for pos in grid)
    # bottom = max(pos[1] for pos in grid)
    # for y in range(top, bottom + 1):
    #    print(f'{y:02d}', "".join(grid.get((x, y), ".") for x in range(left, right + 1)))

    yield sum(grid.get((x, target_y)) == "#" for x in range(left, right))

    class Frequency:
        def __init__(self, x: int) -> None:
            self.x = x
            self.y_candidate_ranges = [(0, max_y)]

        def remove(self, top: int, bottom: int) -> None:
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

        def candidates(self) -> Iterator[int]:
            for top, bottom in self.y_candidate_ranges:
                for y in range(top, bottom + 1):
                    yield self.x * 4000000 + y

        def __bool__(self) -> bool:
            return len(self.y_candidate_ranges) > 0

    frequencies = {x: Frequency(x) for x in range(max_x + 1)}
    for line in content.splitlines():
        xs, ys, xb, yb = (int(x) for x in re.findall(r"-?\d+", line))
        d = abs(xs - xb) + abs(ys - yb)

        for xd in range(d + 1):
            yd = d - xd
            for x in (xs + xd, xs - xd):
                if x in frequencies:
                    frequencies[x].remove(ys - yd, ys + yd)
                    if not frequencies[x]:
                        del frequencies[x]

    candidates: dict[int, list[int]] = {x: list(frequency.candidates()) for x, frequency in frequencies.items()}
    assert len(candidates) == 1, "Multiple candidates found!"
    x, candidates_frequencies = candidates.popitem()
    assert len(candidates_frequencies) == 1, f"Multiple candidates found at x={x}"
    yield candidates_frequencies[0]


test_content = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
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

assert tuple(solve(test_content, target_y=10, max_x=20, max_y=20)) == (26, 56000011)

with open("15.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
