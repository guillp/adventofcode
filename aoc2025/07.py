from collections import defaultdict


def solve(content: str) -> tuple[int, int]:
    grid = {(x, y): c for y, line in enumerate(content.splitlines()) for x, c in enumerate(line)}
    start_x, start_y = next(pos for pos, c in grid.items() if c == "S")

    to_visit = defaultdict[int, defaultdict[int, int]](lambda: defaultdict(int))
    to_visit[start_y][start_x] = 1
    visited_splits = set()
    part2 = 0
    while to_visit:
        y = min(to_visit)
        while to_visit[y]:
            x, count = to_visit[y].popitem()
            below = grid.get((x, y + 1))
            match below:
                case "." | "|":
                    to_visit[y + 1][x] += count
                case "^":
                    visited_splits.add((x, y))
                    to_visit[y][x - 1] += count
                    to_visit[y][x + 1] += count
                case None:
                    part2 += count
        del to_visit[y]

    return len(visited_splits), part2


test_content = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

assert solve(test_content) == (21, 40)


with open("07.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
