from collections import deque
from collections.abc import Iterator


def find_shortcuts(
    path: tuple[complex, ...],
    max_cheat: int,
    min_shortcut_size: int,
) -> dict[int, set[tuple[complex, ...]]]:
    shortcuts = dict[int, set[tuple[complex, ...]]]()
    for i, left in enumerate(path[:-min_shortcut_size]):
        for j, right in enumerate(path[i + min_shortcut_size :]):
            shortcut_duration = int(abs(left.real - right.real) + abs(left.imag - right.imag))
            if shortcut_duration > max_cheat:
                continue
            shortcut = path[path.index(left) : path.index(right)]
            if len(shortcut) <= shortcut_duration:
                continue
            shortcuts.setdefault(len(shortcut) - shortcut_duration, set()).add(shortcut)

    return shortcuts


def solve(content: str, shortcut_size: int = 100) -> Iterator[int]:
    lines = content.strip().splitlines()
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "#"}
    start_pos = next(pos for pos, c in grid.items() if c == "S")
    end_pos = next(pos for pos, c in grid.items() if c == "E")

    pool = deque[tuple[complex, ...]]()
    pool.append((start_pos,))
    while pool:
        path = pool.popleft()
        pos = path[-1]
        for next_pos in (pos + 1, pos - 1, pos + 1j, pos - 1j):
            if next_pos not in grid or next_pos in path:
                continue
            path = (*path, next_pos)
            if next_pos == end_pos:
                pool.clear()
                break
            else:
                pool.append(path)

    shortcuts_part1 = find_shortcuts(path, 2, shortcut_size)
    yield sum(len(shortcuts) for size, shortcuts in shortcuts_part1.items() if size >= shortcut_size)

    shortcuts_part2 = find_shortcuts(path, 20, shortcut_size)
    yield sum(len(shortcuts) for size, shortcuts in shortcuts_part2.items() if size >= shortcut_size)


test_content = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

assert tuple(solve(test_content, 64)) == (1, 86)

with open("20.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
