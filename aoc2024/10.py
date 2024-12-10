def solve(content: str) -> tuple[int, int]:
    heightmap = dict[int, set[complex]]()
    lines = content.strip().splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            heightmap.setdefault(int(c), set()).add(complex(x, y))

    pool = set[tuple[complex, ...]]((pos,) for pos in heightmap[0])
    for height in range(1, 10):
        next_pool = set[tuple[complex, ...]]()
        for trail in pool:
            for next_pos in (trail[-1] + 1, trail[-1] - 1, trail[-1] - 1j, trail[-1] + 1j):
                if next_pos in heightmap[height]:
                    next_pool.add((*trail, next_pos))
        pool = next_pool

    return len({(trail[0], trail[-1]) for trail in pool}), len(pool)


test_content = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

assert solve(test_content) == (36, 81)

with open("10.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
