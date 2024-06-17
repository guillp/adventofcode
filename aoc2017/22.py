from types import SimpleNamespace

directions = SimpleNamespace(
    UP=-1j,
    RIGHT=1,
    DOWN=1j,
    LEFT=-1,
)

turns = SimpleNamespace(RIGHT=1j, LEFT=-1j, REVERSE=-1)

states = SimpleNamespace(
    INFECTED="#",
    CLEAN=".",
    WEAKENED="W",
    FLAGGED="F",
)


def part1(content: str, bursts: int = 10_000) -> int:
    lines = content.strip().splitlines()
    H = len(lines)
    W = len(lines[0])
    assert H % 2 == W % 2 == 1
    grid = {complex(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == states.INFECTED}

    position = complex(W // 2, H // 2)
    direction = directions.UP
    infections = 0

    for _ in range(bursts):
        if position in grid:
            direction *= turns.RIGHT
            grid.remove(position)
        else:
            direction *= turns.LEFT
            grid.add(position)
            infections += 1
        position += direction

    return infections


def part2(content: str, bursts: int = 10000000) -> int:
    lines = content.strip().splitlines()
    H = len(lines)
    W = len(lines[0])
    assert H % 2 == W % 2 == 1
    grid = {
        complex(x, y): states.INFECTED
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c == states.INFECTED
    }

    position = complex(W // 2, H // 2)
    direction = directions.UP
    infections = 0

    for _ in range(bursts):
        match grid.get(position, states.CLEAN):
            case states.CLEAN:
                direction *= turns.LEFT
                grid[position] = states.WEAKENED
            case states.WEAKENED:
                grid[position] = states.INFECTED
                infections += 1
            case states.INFECTED:
                direction *= turns.RIGHT
                grid[position] = states.FLAGGED
            case states.FLAGGED:
                direction *= turns.REVERSE
                del grid[position]
        position += direction

    return infections


test_content = """\
..#
#..
..."""


assert part1(test_content, 7) == 5
assert part1(test_content, 70) == 41
assert part1(test_content) == 5587

assert part2(test_content, 100) == 26
assert part2(test_content) == 2511944


with open("22.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
