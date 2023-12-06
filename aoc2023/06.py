from math import ceil

with open('06.txt') as f: content = f.read()

lines = content.splitlines()
times = (int(x) for x in lines[0].split()[1:])
distance = (int(x) for x in lines[1].split()[1:])


def solve(t: int, d: int) -> int:
    D = t ** 2 - 4 * (d + 0.01)
    assert D > 0
    x1 = ceil((t - D ** .5) / 2)
    x2 = ceil((t + D ** .5) / 2)
    return x2 - x1


s = 1
for t, d in zip(times, distance):
    s *= solve(t, d)
print(s)

t = int(''.join(lines[0].split()[1:]))
d = int(''.join(lines[1].split()[1:]))

print(solve(t, d))
