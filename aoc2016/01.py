with open("1.txt", "rt") as finput:
    content = finput.read()

pos = 0
angle = 1
visited = {0}
part2_found = False
for instruction in content.split(", "):
    direction, steps = instruction[0], instruction[1:]
    angle *= {"L": 1j, "R": -1j}[direction]
    for d in range(int(steps)):
        pos += angle
        if pos in visited and not part2_found:
            print("PART2:", int(abs(pos.real) + abs(pos.imag)))
            part2_found = True
        visited.add(pos)

print("PART1:", int(abs(pos.real) + abs(pos.imag)))
