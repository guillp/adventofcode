from heapq import heappop, heappush

test_content = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

with open("17.txt") as f:
    content = f.read()


def solve(content: str, min_straigth: int = 1, max_straigth: int = 3):
    lines = content.splitlines()
    H = len(lines)
    W = len(lines[0])
    grid = {
        (x, y): int(loss) for y, line in enumerate(lines) for x, loss in enumerate(line)
    }

    start = (0, 0)
    target = (W - 1, H - 1)

    best = sum(grid.values())
    best_directions = None
    DIRECTIONS = {
        ">": (1, 0, "<"),
        "v": (0, 1, "^"),
        "^": (0, -1, "v"),
        "<": (-1, 0, ">"),
    }

    queue = [(0, start, "", 0)]
    visited = set()

    while queue:
        loss, (x, y), directions, streak = heappop(queue)
        last_direction = directions[-1:]

        if ((x, y), last_direction, streak) in visited:
            continue
        visited.add(((x, y), last_direction, streak))
        for next_direction, (dx, dy, opposite_direction) in DIRECTIONS.items():
            if next_direction == last_direction or opposite_direction == last_direction:
                continue
            next_x, next_y, next_loss = x, y, loss
            for i in range(1, max_straigth + 1):
                next_x += dx
                next_y += dy
                if (next_x, next_y) not in grid:  # don't go off grid
                    break

                next_loss += grid[next_x, next_y]
                if next_loss > best:
                    break
                if i <= min_straigth - 1:
                    continue

                next_directions = directions + next_direction * i
                if (next_x, next_y) == target:
                    best = min(best, next_loss)
                    best_directions = next_directions
                else:
                    heappush(queue, (next_loss, (next_x, next_y), next_directions, i))

    return best


assert solve(test_content) == 102
print(solve(content))

assert solve(test_content, 4, 10) == 94
assert (
    solve(
        """\
111111111111
999999999991
999999999991
999999999991
999999999991""",
        4,
        10,
    )
    == 71
)
print(solve(content, 4, 10))
