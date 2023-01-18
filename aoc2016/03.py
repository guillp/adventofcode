with open("03.txt") as f:
    content = f.read()

s = 0
for line in content.splitlines():
    x, y, z = sorted(int(n) for n in line.strip().split())
    if x + y > z:
        s += 1

print(s)


s = 0
numbers = [int(n) for line in content.splitlines() for n in line.strip().split()]
assert len(numbers) % 9 == 0
for i in range(len(numbers) // 9):
    x1, x2, x3, y1, y2, y3, z1, z2, z3 = numbers[i * 9 : (i + 1) * 9]
    for x, y, z in ((x1, y1, z1), (x2, y2, z2), (x3, y3, z3)):
        x, y, z = sorted((x, y, z))
        if x + y > z:
            s += 1

print(s)
