from stringparser import Parser

with open("14.txt", "rt") as finput:
    content = finput.read()

parser = Parser(
    "{} can fly {:d} km/s for {:d} seconds, but then must rest for {:d} seconds."
)

N = 2503

s = 0
for line in content.splitlines():
    name, speed, time, rest = parser(line)
    d, m = divmod(N, time + rest)
    distance = speed * time * d + speed * min(time, m)
    if distance > s:
        s = distance
    # print(name, distance)

print(s)

reindeers = {}
for line in content.splitlines():
    name, speed, time, rest = parser(line)
    reindeers[name] = (speed, time, rest)

state = {name: 0 for name in reindeers}
scores = {name: 0 for name in reindeers}

for i in range(2503):
    max_dist = 0
    for name, distance in state.items():
        speed, time, rest = reindeers[name]
        d, m = divmod(i, time + rest)
        if m < time:
            distance += speed
        state[name] = distance
        if distance > max_dist:
            max_dist = distance
    for name, distance in state.items():
        if distance == max_dist:
            scores[name] += 1

print(max(scores.values()))
