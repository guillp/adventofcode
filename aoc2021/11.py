from collections.abc import Iterable
from itertools import count


def solve(content: str) -> Iterable[int]:
    grid = {complex(x, y): int(c) for y, line in enumerate(content.strip().splitlines()) for x, c in enumerate(line)}
    part1 = 0
    for step in count(1):
        for pos in grid:
            grid[pos] += 1
        to_check = set(grid)
        flashed = set()
        while to_check:
            pos = to_check.pop()
            if grid[pos] > 9 and pos not in flashed:
                flashed.add(pos)
                part1 += 1
                for nb in (
                    pos - 1j,
                    pos - 1j + 1,
                    pos + 1,
                    pos + 1j + 1,
                    pos + 1j,
                    pos + 1j - 1,
                    pos - 1,
                    pos - 1j - 1,
                ):
                    if nb in grid:
                        grid[nb] += 1
                        to_check.add(nb)
        for pos in flashed:
            grid[pos] = 0
        if step == 100:
            yield part1

        if len(flashed) == 100:
            yield step
            return


assert tuple(
    solve("""\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""),
) == (1656, 195)

with open("11.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
