from collections.abc import Iterator
from heapq import heappop, heappush


def solve(content: str, n: int = 1024, width: int = 70, *, debug: bool = False) -> Iterator[int | str]:
    lines = content.strip().splitlines()
    corrupted = set()
    for line in lines[:n]:
        x, y = map(int, line.split(","))
        corrupted.add((x, y))
    end = (width, width)
    paths = labyrinth(width, corrupted, end)
    yield len(min(paths, key=len)) - 1

    for line in lines[n:]:
        x, y = map(int, line.split(","))
        corrupted.add((x, y))
        for path in paths.copy():
            if (x, y) in path:
                paths.remove(path)
        if not paths:
            paths = labyrinth(width, corrupted, end)
            if not paths:
                yield f"{x},{y}"
                if debug:
                    for c in range(width + 1):
                        print(
                            "".join(
                                "!" if (r, c) == (x, y) else "#" if (r, c) in corrupted else "."
                                for r in range(width + 1)
                            ),
                        )
                return


def labyrinth(width: int, corrupted: set[tuple[int, int]], end: tuple[int, int]) -> set[tuple[tuple[int, int], ...]]:
    pool: list[tuple[int, tuple[tuple[int, int], ...]]] = [(width * 2, ((0, 0),))]
    depths = {(0, 0): 0}
    best_paths = set[tuple[tuple[int, int], ...]]()
    while pool:
        _, path = heappop(pool)
        x, y = path[-1]
        if depths.get((x, y), width**2) < len(path) - 1:
            continue
        for nx, ny in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
            if not (0 <= nx <= width and 0 <= ny <= width) or (nx, ny) in path or (nx, ny) in corrupted:
                continue
            if depths.get((nx, ny), width**2) <= len(path):
                continue
            depths[(nx, ny)] = len(path)
            if (nx, ny) != end:
                heappush(pool, (width * 2 - nx - ny, (*path, (nx, ny))))
            else:
                best_paths |= {(*path, (nx, ny))}

    return best_paths


test_content = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

assert next(solve(test_content, 12, 6)) == 22

with open("18.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
