import re
from itertools import permutations


def part1(content: str) -> int:
    nodes = [
        tuple(int(x) for x in re.findall(r"\d+", line)) for line in content.splitlines() if line.startswith("/dev/grid")
    ]
    return sum(
        1
        for (x1, y1, _, used1, avail1, _), (
            x2,
            y2,
            _,
            used2,
            avail2,
            _,
        ) in permutations(nodes, 2)
        if 0 < used1 <= avail2
    )


def print_grid(G: dict[tuple[int, int], str], W: int, H: int) -> None:
    for y in range(H):
        print("".join(G[x, y] for x in range(W)))


def move(G: dict[tuple[int, int], str], direction: str) -> None:
    x, y = next((x, y) for ((x, y), c) in G.items() if c == "_")
    dx = dy = 0
    if direction == "UP":
        dy = -1
    elif direction == "DOWN":
        dy = 1
    elif direction == "RIGHT":
        dx = 1
    elif direction == "LEFT":
        dx = -1
    G[x + dx, y + dy], G[x, y] = G[x, y], G[x + dx, y + dy]


def part2(content: str) -> int:
    G: dict[tuple[int, int], str] = {}
    x_max = y_max = 0
    for line in content.splitlines():
        if not line.startswith("/dev/grid"):
            continue
        x, y, size, used, _, _ = (int(x) for x in re.findall(r"\d+", line))
        G[x, y] = "X" if x == y == 0 else "_" if used < 50 else "#" if used > 100 else "."
        x_max = max(x_max, x)
        y_max = max(y_max, y)

    G[x_max, 0] = "T"
    W, H = x_max + 1, y_max + 1
    print_grid(G, W, H)

    for _ in range(6):
        move(G, "LEFT")
    for _ in range(6):
        move(G, "UP")
    for _ in range(22):
        move(G, "RIGHT")
    for _ in range(35):
        move(G, "DOWN")
        move(G, "LEFT")
        move(G, "LEFT")
        move(G, "UP")
        move(G, "RIGHT")
    print_grid(G, W, H)

    return 6 + 6 + 22 + 35 * 5


with open("22.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
