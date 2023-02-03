h, w = [int(x) for x in input().split()]
grid = {complex(x, y): c for y in range(h) for x, c in enumerate(input())}

for pos, c in grid.items():
    if c == "P":
        start = pos
        grid[pos] = "."
    elif c == "X":
        end = pos
        grid[pos] = "."


def iter_next_pos(pos: complex):
    for dir in (1, -1, -1j, 1j):
        new_pos = pos
        while grid.get(new_pos + dir) in ".o":
            new_pos += dir
            if grid.get(new_pos) == "o":
                break
        if pos != new_pos:
            yield new_pos


i = 0
pool = {start}
visited = {start}
while end not in pool:
    pool = set(new_pos for pos in pool for new_pos in iter_next_pos(pos)) - visited
    visited |= pool
    i += 1

print(i)