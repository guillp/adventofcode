with open('10.txt') as f: content = f.read()

# read input
lines = content.splitlines()
grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}

# find start location and pipe form
start = next(pos for pos, c in grid.items() if c == 'S')

match grid[start - 1], grid[start - 1j], grid[start + 1], grid[start + 1j]:
    case "-" | "F" | "L", "|" | "F" | "7", _, _:
        start_pipe = "J"
    case "-" | "F" | "L", _, "-" | "J" | "7", _:
        start_pipe = "-"
    case "-" | "F" | "L", _, _, "|" | "J" | "L":
        start_pipe = "7"
    case _, "|" | "F" | "7", "-" | "7" | "J", _:
        start_pipe = "L"
    case _, "|" | "F" | "7", _, "|" | "L" | "J":
        start_pipe = "|"
    case _, _, "-" | "7" | "J", "|", "L", "J":
        start_pipe = "F"
    case _:
        assert False

grid[start] = start_pipe

NORTH = -1j
SOUTH = 1j
EAST = 1
WEST = -1

# follow the pipe from the start until we come back to the start
loop = start,
dir = {"J": NORTH, "-": EAST, "7": SOUTH, "L": EAST, "|": NORTH, "F": EAST}.get(start_pipe)
while len(loop) == 1 or loop[-1] != start:
    pos = loop[-1]
    next_dir = {
        "J": {EAST: NORTH, SOUTH: WEST},
        "F": {NORTH: EAST, WEST: SOUTH},
        "L": {SOUTH: EAST, WEST: NORTH},
        "7": {EAST: SOUTH, NORTH: WEST},
        "|": {NORTH: NORTH, SOUTH: SOUTH},
        "-": {EAST: EAST, WEST: WEST},
    }[grid[pos + dir]][dir]
    next_pos = pos + dir
    dir = next_dir
    loop += next_pos,

print((len(loop) - 1) // 2)  # -1 because path contains "start" twice

# cross the grid line by line
# if we cross an even number of pipes, we are outside
inside = 0
for y, line in enumerate(lines):
    pipes = 0
    for x, c in enumerate(line):
        p = complex(x, y)
        if c == 'S': c = grid.get(p)
        if c in '|F7' and p in loop:  # count the number of vertical pipes we cross. F
            pipes += 1
        if p not in loop and pipes % 2 == 1:  # if we crossed pipes an odd number of times, we are inside
            inside += 1

print(inside)
