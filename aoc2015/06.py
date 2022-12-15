from stringparser import Parser

with open("06.txt", "rt") as finput:
    content = finput.read()

parser = Parser("{} {:d},{:d} through {:d},{:d}")

lights = [False for _ in range(1000 * 1000)]
for line in content.splitlines():
    instruction, x1, y1, x2, y2 = parser(line)
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if instruction == "turn on":
                lights[y * 1000 + x] = True
            elif instruction == "turn off":
                lights[y * 1000 + x] = False
            elif instruction == "toggle":
                lights[y * 1000 + x] = not lights[y * 1000 + x]


print(sum(lights))

lights = [0 for _ in range(1000 * 1000)]
for line in content.splitlines():
    instruction, x1, y1, x2, y2 = parser(line)
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if instruction == "turn on":
                lights[y * 1000 + x] += 1
            elif instruction == "turn off":
                if lights[y * 1000 + x] > 0:
                    lights[y * 1000 + x] -= 1
            elif instruction == "toggle":
                lights[y * 1000 + x] += 2

print(sum(lights))
