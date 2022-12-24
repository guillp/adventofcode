from collections import defaultdict
from functools import cache
from typing import Iterable

content = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

with open("24.txt") as f:
    content = f.read()

grid = defaultdict(set)
max_x = max_y = 0
for y, line in enumerate(content.splitlines(), start=-1):
    for x, c in enumerate(line, start=-1):
        if c in "><^v":
            grid[x, y].add(c)
        elif c == ".":
            max_x = max(max_x, x)
            max_y = max(max_y, y - 1)

start_x, start_y = 0, -1
end_x, end_y = max_x, max_y + 1


@cache
def grid_at_minute(m: int):
    previous_grid = grid_at_minute(m - 1) if m > 1 else grid
    new_grid = defaultdict(set)
    for (x, y), blizzards in previous_grid.items():
        for blizzard in blizzards:
            new_x, new_y = x, y
            if blizzard == ">":
                new_x = (x + 1) if x < max_x else 0
            elif blizzard == "<":
                new_x = (x - 1) if x > 0 else max_x
            elif blizzard == "v":
                new_y = (y + 1) if y < max_y else 0
            elif blizzard == "^":
                new_y = (y - 1) if y > 0 else max_y

            new_grid[new_x, new_y].add(blizzard)

    return new_grid


def print_grid(grid: dict[tuple[int, int], str]):
    print("#." + "#" * (max_x + 1))
    for y in range(max_y + 1):
        print(end="#")
        for x in range(max_x + 1):
            blizzards = grid.get((x, y))
            if blizzards is None:
                print(end=".")
            elif len(blizzards) == 1:
                print(end=tuple(blizzards)[0])
            else:
                print(end=str(len(blizzards)))
        print("#")
    print("#" * (max_x + 1) + ".#")


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def neighbours(x: int, y: int, m: int) -> Iterable[tuple[int, int]]:
    for x, y in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1), (x, y)):
        if (x, y) in grid_at_minute(m):  # would hit a blizzard
            continue
        if (0 <= x <= max_x and 0 <= y <= max_y) or (x, y) in (
            (start_x, start_y),
            (end_x, end_y),
        ):
            yield x, y


def find_path(
    start_x: int, start_y: int, end_x: int, end_y: int, start_time: int = 0
) -> int:
    pool = {(0, start_x, start_y)}

    best_steps = 10**20
    while pool:
        m, x, y = min(
            pool, key=lambda mxy: (mxy[0], distance(mxy[1], mxy[2], end_x, end_y))
        )
        pool.remove((m, x, y))

        if m >= best_steps:
            continue

        for next_x, next_y in neighbours(x, y, start_time + m + 1):
            # print(f"{m+1}: from {x},{y} can reach {next_x},{next_y}")
            if (next_x, next_y) == (end_x, end_y):
                best_steps = m + 1
                # print("best steps:", m+1)
            else:
                pool.add((m + 1, next_x, next_y))

    return best_steps


there = find_path(start_x, start_y, end_x, end_y)
print(there)
back = find_path(end_x, end_y, start_x, start_y, there)
again = find_path(start_x, start_y, end_x, end_y, there + back)
print(there + back + again)
