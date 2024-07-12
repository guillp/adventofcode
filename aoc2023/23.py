from heapq import heappop, heappush

SLOPES = {1: ">", -1: "<", 1j: "v", -1j: "^"}


def part1(content: str) -> int:
    lines = content.splitlines()
    H = len(lines)
    start_pos = complex(lines[0].index("."), 0)
    target_pos = complex(lines[-1].index("."), H - 1)
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "#"}

    heap: list[
        tuple[
            int,  #
            str,
            tuple[complex, ...],
        ]
    ] = []
    heappush(heap, (0, "", (start_pos,)))
    best = 0
    while heap:
        l, trace, path = heappop(heap)
        current_pos = path[-1]
        for d in (1, 1j, -1, -1j):
            next_pos = current_pos + d
            if next_pos not in grid:
                continue  # don't step out of path
            if next_pos in path:
                continue  # don't step twice on the same tile
            if SLOPES[-d] == grid[next_pos]:
                continue  # don't try to walk slopes uphill
            if next_pos == target_pos:
                if l - 1 < best:
                    best = l - 1
            else:
                heappush(heap, (l - 1, trace + SLOPES[d], path + (next_pos,)))

    return -best


def part2(content: str) -> int:
    lines = content.splitlines()
    height = len(lines)
    start_pos = complex(lines[0].index("."), 0)
    target_pos = complex(lines[-1].index("."), height - 1)
    grid = {complex(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c != "#"}

    # turn the labyrinth into a graph using a quick DFS
    G: dict[complex, dict[complex, int]] = {start_pos: {}, target_pos: {}}
    pool: list[tuple[complex, ...]] = [(start_pos,), (target_pos,)]
    while pool:
        path = pool.pop()
        current_pos = path[-1]
        next_positions = {
            current_pos + d for d in (1, 1j, -1, -1j) if current_pos + d in grid and current_pos + d not in path
        }
        match len(next_positions):
            case 0:
                continue  # dead end
            case 1:  # on a single path
                pool.append(path + (next_positions.pop(),))
            case 2 | 3:  # reached an intersection
                if current_pos not in G:
                    for p in next_positions:
                        pool.append((current_pos, p))
                G.setdefault(current_pos, {})
                G[current_pos][path[0]] = len(path) - 1
                G[path[0]][current_pos] = len(path) - 1

    # do another DFS to find the longest path in that graph
    pool2: list[tuple[int, tuple[complex, ...]]] = [(0, (start_pos,))]
    longest = 0
    while pool:
        l, path = pool2.pop()
        current_pos = path[-1]
        for next_pos, steps in G[current_pos].items():
            if next_pos in path:
                continue  # don't walk twice on the same tile
            if next_pos == target_pos:
                if l + steps > longest:
                    longest = l + steps
            else:
                pool2.append((l + steps, path + (next_pos,)))

    return longest


test_content = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

assert (part1(test_content)) == 94
assert part2(test_content) == 154

with open("23.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
