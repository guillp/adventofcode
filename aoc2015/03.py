with open("03.txt", "rt") as finput:
    content = finput.read()

pos = 0 + 0j
grid = {pos: True}

for move in content:
    if move == "^":
        pos -= 1j
    elif move == "v":
        pos += 1j
    elif move == ">":
        pos += 1
    elif move == "<":
        pos -= 1
    grid[pos] = True

print(len(grid))


pos1 = pos2 = 0 + 0j
grid = {pos1: True}

for move in content[::2]:
    if move == "^":
        pos1 -= 1j
    elif move == "v":
        pos1 += 1j
    elif move == ">":
        pos1 += 1
    elif move == "<":
        pos1 -= 1
    grid[pos1] = True

for move in content[1::2]:
    if move == "^":
        pos2 -= 1j
    elif move == "v":
        pos2 += 1j
    elif move == ">":
        pos2 += 1
    elif move == "<":
        pos2 -= 1
    grid[pos2] = True

print(len(grid))
